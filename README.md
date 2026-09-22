# ConcordBatch

ConcordBatch is a reusable, contract-only GenLayer Intelligent Contract for
clearing two compatible actions from three wallet-authenticated participants.
It is not an app and has no frontend. Participants submit bounded descriptions
of actions, preconditions, and side effects; validators classify the complete
three-pair conflict/order graph; deterministic contract code selects the
highest-priority compatible pair, grants ordered one-time execution tickets,
and opens fixed GEN credits.

## Deployment

- Network: Studio Dev (chain ID `61997`)
- Contract: [`0x678607d653706E1Bd4B0812035e5b4bE661438bc`](https://explorer-studio-dev.genlayer.com/address/0x678607d653706E1Bd4B0812035e5b4bE661438bc)
- Deploy transaction: [`0xedc894e3e468dafb3d1c17b8f17969b1d86e10442478fb82b29e057d6f9c0231`](https://explorer-studio-dev.genlayer.com/tx/0xedc894e3e468dafb3d1c17b8f17969b1d86e10442478fb82b29e057d6f9c0231)
- Explorer result: `FINALIZED`, consensus `Accepted`, execution `SUCCESS`
- Active source commit: `479caf08c0015e13321051273da0692c7b1b9278`

The sanitized deployment and lifecycle records are in
[`docs/evidence/studio-dev`](docs/evidence/studio-dev). Two superseded
revisions are archived there and honestly labeled abandoned; neither will
receive further value.

## Why GenLayer consensus is essential

String equality cannot decide whether two differently worded actions can
coexist, conflict, or require an order. The leader classifies the operational
meaning of all three pairs as `INDEPENDENT`, `LEFT_BEFORE_RIGHT`,
`RIGHT_BEFORE_LEFT`, or `INCOMPATIBLE`. Validators independently repeat that
semantic judgment and compare the normalized meaning tuple: exact batch,
attempt, policy and intent-set bindings plus every pair relation. Rationale
wording is ignored. Different semantic decisions therefore cannot both pass.

The model never chooses a payee, amount, priority, ticket, or state transition.
Contract code validates exact pair coverage, rejects cycles, derives basis
enums, selects by the locked priority permutation, and enforces the fixed 2 GEN
accounting consequence. Invalid or unavailable output is `RETRYABLE` and moves
no value.

## Real Studio Dev example

Input (real):

- A: rotate the signing key and revoke the old key immediately.
- B: deploy a client configuration that pins the old key for 24 hours.
- C: update documentation with no runtime side effect.
- Locked priority: `A,B,C`; purse: `2 GEN`.

Output (real, batch `concord-demo-479caf0`):

- A/B: `INCOMPATIBLE`.
- A/C and B/C: `INDEPENDENT`.
- Selected order: A, then C.
- State: `CLEARED`; attempt: `VALID`.
- Credits: A `1 GEN`, C `1 GEN`; locked `0 GEN`.
- Conservation: received `2 GEN` = credits `2 GEN` + locked `0 GEN` + withdrawn `0 GEN`.

These are canonical onchain reads, not expected values or a local simulation.

## Public interface

Writes:

- `create_batch(...)` receives exactly 2 GEN and locks policy, roles, priority,
  and deadlines.
- `submit_intent(...)` accepts one immutable intent from each registered slot.
- `review_batch(...)` runs the semantic validator before any consequence.
- `recover_incomplete(...)` and `recover_unresolved(...)` provide bounded
  sponsor refunds at their exact deadlines.
- `consume_ticket(...)` enforces selected ownership and execution order.
- `withdraw_credit()` debits a caller-owned credit before transfer.

Views: `get_batch`, `get_intent`, `get_attempt`, `get_pair_relation`,
`get_ticket`, `get_credit`, and `get_accounting`.

## Reuse

The primitive can coordinate an A2A tool gateway, a DAO automation queue, or a
turn-based AI game engine. Consumers read finalized tickets and credits; they do
not need to trust an offchain scheduler or copy validator logic.

## Local verification

Use Python 3.12 and Node.js, then install the pinned dependencies:

```powershell
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements-dev.txt
npm ci
npm run check
```

The gate performs ASCII/header checks, GenVM semantic lint, direct-mode
lifecycle/safety tests, and raw/normalized deployment receipt parser tests.
The current verified result is 26 direct tests plus 4 receipt tests, all
passing; `genvm-lint` recognizes exactly `ConcordBatch` with 7 views and 7
writes.

## Honest limits

V1 is fixed to three participants and two slots. It judges declared intent
meaning, not actual external execution or undisclosed side effects. Priority is
sponsor-locked and transparent, not globally optimal. No frontend, callback,
external adopter, legal guarantee, multi-network proof, or Portal acceptance is
claimed.

The full specification, all 14 gate decisions, evidence authority matrix,
write-method safety matrix, temporal rules, and value-destination matrix are in
[`docs/README.md`](docs/README.md).
