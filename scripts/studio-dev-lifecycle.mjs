import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createAccount, createClient, isSuccessful } from "genlayer-js";
import { studioDevnet } from "genlayer-js/chains";

const PROJECT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DEPLOYMENT = path.join(PROJECT, "docs", "evidence", "studio-dev", "deployment.json");
const EVIDENCE = path.join(PROJECT, "docs", "evidence", "studio-dev", "lifecycle.json");
const STATE = path.join(PROJECT, ".local", "studio-dev-lifecycle.json");
const GEN = 10n ** 18n;
const BUDGET = 2n * GEN;

function parseEnv(text) {
  const values = {};
  for (const line of String(text).split(/\r?\n/)) {
    const index = line.indexOf("=");
    if (index <= 0 || line.trimStart().startsWith("#")) continue;
    const key = line.slice(0, index).trim();
    let value = line.slice(index + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
    values[key] = value;
  }
  return values;
}

for (const file of [path.join(PROJECT, ".env"), path.resolve(PROJECT, "..", ".env")]) {
  if (!fs.existsSync(file)) continue;
  for (const [key, value] of Object.entries(parseEnv(fs.readFileSync(file, "utf8")))) {
    if (value && !process.env[key]) process.env[key] = value;
  }
}

function privateKey(name) {
  const value = process.env[name]?.trim() ?? "";
  if (!/^(0x)?[0-9a-fA-F]{64}$/.test(value)) throw new Error(`authorized ${name} is absent or invalid`);
  return value.startsWith("0x") ? value : `0x${value}`;
}

function readJson(file, fallback = {}) {
  return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, "utf8")) : fallback;
}

function writeJson(file, value, mode) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`, { encoding: "utf8", ...(mode ? { mode } : {}) });
}

function formatGen(value) {
  const amount = BigInt(value);
  const whole = amount / GEN;
  const fraction = amount % GEN;
  return fraction === 0n ? `${whole} GEN` : `${whole}.${fraction.toString().padStart(18, "0").replace(/0+$/, "")} GEN`;
}

async function main() {
  const deployment = readJson(DEPLOYMENT);
  if (deployment.chainId !== 61997 || !/^0x[0-9a-fA-F]{40}$/.test(deployment.contractAddress ?? "")) {
    throw new Error("valid Studio Dev deployment evidence is required");
  }
  const accounts = {
    participantA: createAccount(privateKey("STUDIONET_PRIVATE_KEY")),
    participantB: createAccount(privateKey("STUDIONET_INTEGRATOR_PRIVATE_KEY")),
    participantC: createAccount(privateKey("STUDIONET_STEWARD_PRIVATE_KEY")),
  };
  const addresses = Object.values(accounts).map((account) => account.address.toLowerCase());
  if (new Set(addresses).size !== 3) throw new Error("three distinct authorized EOAs are required");
  const endpoint = process.env.STUDIO_DEV_RPC_URL?.trim() || studioDevnet.rpcUrls.default.http[0];
  const clients = Object.fromEntries(Object.entries(accounts).map(([name, account]) => [
    name, createClient({ chain: studioDevnet, endpoint, account }),
  ]));
  const address = deployment.contractAddress;
  const state = readJson(STATE);
  state.batchId ??= `concord-demo-${deployment.sourceCommit.slice(0, 7)}`;
  state.hashes ??= {};
  writeJson(STATE, state, 0o600);

  async function write(role, method, args, value = 0n) {
    const client = clients[role];
    const quote = await client.estimateTransactionFeesForWrite({ address, functionName: method, args, value });
    const hash = await client.writeContract({
      address, functionName: method, args, value,
      fees: { distribution: quote.distribution, feeValue: quote.feeValue },
    });
    console.log(`LIFECYCLE_SUBMITTED role=${role} method=${method} value=${formatGen(value)} hash=${hash}`);
    const receipt = await client.waitForTransactionReceipt({ hash, waitUntil: "finalized", interval: 3000, retries: 160 });
    if (!isSuccessful(receipt)) throw new Error(`${role} ${method} finalized without successful execution`);
    const key = `${role}_${method}_${Object.keys(state.hashes).length + 1}`;
    state.hashes[key] = String(hash);
    writeJson(STATE, state, 0o600);
    console.log(`LIFECYCLE_FINALIZED role=${role} method=${method} feeDeposit=${formatGen(quote.feeValue)} hash=${hash}`);
  }

  async function batch() {
    try {
      return JSON.parse(String(await clients.participantA.readContract({ address, functionName: "get_batch", args: [state.batchId] })));
    } catch {
      return null;
    }
  }

  const balances = await Promise.all(Object.entries(clients).map(async ([role, client]) => [
    role, await client.getBalance({ address: accounts[role].address }),
  ]));
  console.log(`LIFECYCLE_PREFLIGHT ${balances.map(([role, balance]) => `${role}=${formatGen(balance)}`).join(" ")}`);
  if (balances.find(([role, balance]) => role === "participantA")[1] < BUDGET) throw new Error("sponsor balance is below 2 GEN");
  if (balances.some(([, balance]) => balance <= 0n)) throw new Error("an authorized participant has no GEN for fees");

  let current = await batch();
  if (!current) {
    const now = Math.floor(Date.now() / 1000);
    state.submitDeadline = now + 86400;
    state.reviewDeadline = now + 172800;
    writeJson(STATE, state, 0o600);
    await write("participantA", "create_batch", [
      state.batchId,
      accounts.participantA.address,
      accounts.participantB.address,
      accounts.participantC.address,
      "A,B,C",
      "Clear two intents only when their stated preconditions and side effects can coexist under the shared service policy.",
      state.submitDeadline,
      state.reviewDeadline,
    ], BUDGET);
    current = await batch();
  }
  const intents = {
    participantA: ["Rotate the service signing key.", "The maintenance window is open.", "The old key is revoked immediately."],
    participantB: ["Deploy a client configuration.", "The current signing key is accepted.", "The client pins the old key for 24 hours."],
    participantC: ["Update public documentation copy.", "The documentation repository is writable.", "No runtime resource changes."],
  };
  for (const role of ["participantA", "participantB", "participantC"]) {
    const slot = role.slice(-1);
    if (Number(current.submitted_count) < { A: 1, B: 2, C: 3 }[slot]) {
      await write(role, "submit_intent", [state.batchId, ...intents[role]]);
      current = await batch();
    }
  }
  if (current.phase === "READY" || current.phase === "RETRYABLE") {
    await write("participantA", "review_batch", [state.batchId]);
    current = await batch();
  }
  const attemptId = `${state.batchId}-attempt-${current.attempt_count}`;
  const attempt = JSON.parse(String(await clients.participantA.readContract({ address, functionName: "get_attempt", args: [attemptId] })));
  const accounting = JSON.parse(String(await clients.participantA.readContract({ address, functionName: "get_accounting", args: [] })));
  const credits = {};
  for (const role of Object.keys(accounts)) {
    credits[role] = JSON.parse(String(await clients.participantA.readContract({ address, functionName: "get_credit", args: [accounts[role].address] })));
  }
  const evidence = {
    network: "studio-dev",
    chainId: 61997,
    contractAddress: address,
    explorerUrl: deployment.explorerUrl,
    batchId: state.batchId,
    roles: Object.fromEntries(Object.entries(accounts).map(([role, account]) => [role, account.address])),
    sponsorRole: "participantA",
    demoPurse: "2 GEN",
    phase: current.phase,
    selectedOrder: [current.selected_first, current.selected_second].filter(Boolean),
    attempt: { attemptId, outcome: attempt.outcome, meaningDigest: attempt.meaning_digest },
    credits: Object.fromEntries(Object.entries(credits).map(([role, credit]) => [role, formatGen(credit.amount)])),
    accounting: {
      totalReceived: formatGen(accounting.total_received),
      totalLocked: formatGen(accounting.total_locked),
      totalCredits: formatGen(accounting.total_credits),
      totalWithdrawn: formatGen(accounting.total_withdrawn),
    },
    transactions: state.hashes,
    evidenceIsSanitized: true,
  };
  writeJson(EVIDENCE, evidence);
  console.log(`LIFECYCLE_COMPLETE batch=${state.batchId} phase=${current.phase} outcome=${attempt.outcome} accounting=${JSON.stringify(evidence.accounting)}`);
}

main().catch((error) => {
  console.error(`LIFECYCLE_FAILED ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
