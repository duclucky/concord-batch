# ConcordBatch specification

## Identity

- Idea ID: `IDEA-031`
- Project name: ConcordBatch
- Project slug: `concord-batch`
- Category: Intelligent Contracts
- Status: DESIGN
- Repository: local child Git repository; public remote pending Phase 9
- Target network: Studio Dev, chain ID 61997

## One-sentence product hook

ConcordBatch turns three wallet-authenticated natural-language action intents
into one validator-agreed conflict/order graph, then clears two executable
intents, one-time tickets, and two fixed 1 GEN credits without trusting a
central scheduler.

## Track lock and compatibility decision

This repository is contract-only. It contains no user-facing frontend, hosted
application, or Vercel deployment. The production contract will use the current
GenVM v0.3 API family and a concrete `py-genlayer` runner hash verified against
the official SDK, installed semantic linter, and a bounded Studio Dev smoke.
The v0.3 unit uses `import genlayer as gl`, `gl.contract.Contract`, and sandboxed
`gl.vm.run_nondet_default`; legacy v0.2 star-import examples are not mixed into
that unit. Any observed Studio template drift is recorded before deployment.

## Trust problem

- Decision that must not depend on one party: which two of three competing
  natural-language intents can safely execute together, and in which order.
- Why database/ordinary EVM/backend LLM is insufficient: deterministic code can
  enforce a returned graph, but cannot interpret semantic side effects,
  preconditions, or ordering. A private scheduler or single LLM can favor an
  actor and redirect rights and 2 GEN.
- Value/rights/access at risk: two one-time execution tickets and a fixed 1 GEN
  credit for each selected participant from the sponsor's 2 GEN purse.

## Fingerprint

- Trust problem: neutral semantic concurrency control before execution rights
  and rewards move.
- Actors/adversary: sponsor plus three fixed participants competing for two
  slots and credits.
- Evidence class + authenticity mechanism: exact bounded policy/intent bytes
  authored by role-checked transactions and bound to contract, batch, actor,
  slot, revision, digest, and deadline.
- Consensus question: the complete relation for each of the three exact intent
  pairs under the locked policy.
- State machine: isolated batches, immutable intents, append-only attempts,
  semantic clearing, ticket consumption, refund recovery, credits, withdrawal.
- Direct consequence: two ordered one-time execution tickets and two 1 GEN
  credits, or a full sponsor refund.
- Reuse surface: batch, intent, relation, attempt, ticket, credit, accounting,
  consume, recovery, and withdrawal methods/views.

## Mandatory gate matrix

| Gate | PASS/FAIL | Evidence/reason |
| --- | --- | --- |
| Replacement | PASS | Replacing GenLayer with a scheduler database or one LLM restores unilateral control over conflict edges, tickets, and credits. |
| Judgment | PASS | Semantic preconditions, side effects, and ordering cannot be derived from deterministic field equality. |
| Evidence availability | PASS | Exact bounded policy/intents are canonical contract state captured before nondeterminism; deterministic readiness checks separate missing input from model/parser failure. |
| Evidence authenticity | PASS | Sender/role, batch, slot, revision, digest, policy, and deadline are verified before review; no external fact or claimant-hosted artifact is accepted. |
| Equivalence | PASS | Validators independently produce and compare the complete normalized three-pair meaning graph; different relations cannot both pass. |
| Consequence | PASS | The graph directly creates two execution rights and two 1 GEN credits, or refunds the full purse. |
| Adversarial | PASS | Three participants compete for two slots and two credits; sponsor/participants can benefit from bias. |
| State model | PASS | Per-batch isolation, immutable role-authored inputs, append-only attempts, local time guards, single settlement, explicit refunds, pull credits, and debit-before-transfer cover lifecycle/value. |
| Reuse | PASS | A2A gateways, DAO queues, and AI game engines consume the same stable interface. |
| Contract count | PASS | One contract owns judgment, rights, accounting, recovery, and withdrawal; a second contract adds no trust boundary. |
| Differentiation | PASS | Complete semantic conflict/order graph clearing for two of three intents differs structurally from matching, policy intersection, post-hoc blame, creative merge/fork, and generic dispute escrow. |
| Claim-to-code | PASS | The matrix below maps every retained claim to a method/state, view, test, and network evidence item. |
| Full lifecycle | PASS | Planned lifecycle covers funding, three submissions, consensus review, graph/order/tickets, consumption, two withdrawals, and zero accounting. |
| Scope honesty | PASS | Only exact contractual descriptions are judged; external execution, undeclared effects, global optimality, adoption, and Portal acceptance are not claimed. |

One failed gate returns the candidate to Phase 2. No frontend or extra contract
may compensate for a failure.

## Actors, roles and incentives

| Actor | Permissions | Value at risk | Incentive to bias |
| --- | --- | --- | --- |
| Sponsor | Create one batch with exact 2 GEN, lock policy/participants/priority/deadlines, recover only through specified paths, withdraw sponsor credit | 2 GEN coordination purse | Prefer a particular pair or avoid paying |
| Participant A | Submit slot A intent once, consume a selected ticket, withdraw credit | Potential ticket and 1 GEN credit | Have own intent classified compatible/selected |
| Participant B | Submit slot B intent once, consume a selected ticket, withdraw credit | Potential ticket and 1 GEN credit | Same |
| Participant C | Submit slot C intent once, consume a selected ticket, withdraw credit | Potential ticket and 1 GEN credit | Same |
| Review caller | Trigger review after readiness; no power to select outcome | Transaction fee only | May prefer an outcome but cannot supply graph or recipients |
| Validators | Independently classify exact pairs under locked policy | Protocol stake/reputation outside application ledger | A leader may propose a biased/incomplete graph |

## Scope and non-goals

### In scope

- Exactly three named participants and exactly two execution slots per batch.
- The three participant addresses must be distinct; the sponsor may also occupy
  one participant role, which keeps the primitive usable with three EOAs.
- One bounded policy and one bounded intent per participant.
- Complete classification of the three unordered pairs.
- Deterministic pair selection, canonical order, two tickets, two 1 GEN
  credits, retry/refund recovery, ticket consumption, and withdrawals.

### Out of scope

- No frontend, hosted app, or Vercel.
- No proof that an intent was executed outside this contract.
- No claim that a participant disclosed every real side effect.
- No arbitrary participant count, global schedule optimization, external tool
  execution, legal effect, identity proof beyond wallet roles, or adoption.
- No claimant-hosted JSON, screenshots, receipts, or offchain signatures as
  consequential authority.

## State model

### Stable IDs

- `batch_id`: caller-supplied non-empty ASCII identifier, globally unique.
- Slot IDs: fixed `A`, `B`, `C`, derived from locked participant addresses.
- `intent_id`: `batch_id + "-" + slot`, derived by contract code.
- `attempt_id`: `batch_id + "-attempt-" + monotonically increasing count`.
- Pair IDs: canonical lexical `left_intent_id + "|" + right_intent_id`.

### Structured storage

- `Batch`: sponsor, participants A/B/C, priority permutation, policy text and
  digest, submit/review deadlines, status, submission count, attempt count,
  selected intent IDs/order, purse, total credit, total withdrawn.
- `Intent`: stable ID, batch ID, slot, author, action, preconditions, side
  effects, revision, digest, submitted timestamp.
- `Attempt`: stable ID, batch/intent-set/policy digests, source coverage,
  normalized pair relations, outcome, timestamp.
- `Ticket`: batch/intent ID, execution order 1 or 2, selected flag, consumed
  flag, consumer participant, consumed timestamp.
- `credits`: address-string keyed `TreeMap[str, bigint]`.
- All persisted amounts are `bigint`; bounded counters use sized integers; all
  `TreeMap` keys are `str`; storage structs use the current storage decorator.

### State machine

```text
ABSENT --create_batch(2 GEN)/sponsor--> OPEN
OPEN --three valid submit_intent calls--> READY
READY --review_batch/meaning agrees and safe pair exists--> CLEARED
READY --review_batch/valid graph has no safe pair--> NO_PAIR_REFUNDED
READY --review_batch/model/source normalization cannot safely decide--> RETRYABLE
RETRYABLE --review_batch before review deadline--> CLEARED | NO_PAIR_REFUNDED | RETRYABLE
OPEN --recover_incomplete at/after submit deadline with fewer than 3 intents--> INCOMPLETE_REFUNDED
READY|RETRYABLE --recover_unresolved at/after review deadline--> UNRESOLVED_REFUNDED
CLEARED --consume_ticket in order/selected participant--> CLEARED with ticket consumed
credit > 0 --withdraw_credit/credit owner--> credit = 0 and withdrawn increases
```

### Temporal entrypoint rules

- Canonical transaction-time source: `gl.message.datetime`, normalized by one
  deterministic helper.
- Default interval: a deadline-bounded action is valid only when
  `now < deadline`; equality is late.
- `create_batch`: `now < submit_deadline < review_deadline`.
- `submit_intent`: entrypoint checks `now < submit_deadline`, even if status is
  stale `OPEN`.
- `review_batch`: entrypoint checks `now < review_deadline`, even if status is
  stale `READY` or `RETRYABLE`.
- `recover_incomplete`: sponsor only, `now >= submit_deadline`, status `OPEN`,
  fewer than three submissions, unsettled purse.
- `recover_unresolved`: sponsor only, `now >= review_deadline`, status `READY`
  or `RETRYABLE`, unsettled purse.
- `consume_ticket` and `withdraw_credit`: genuinely non-temporal; legality is
  controlled by finalized state/ticket order/credit.

### Illegal transitions

- Duplicate batch, duplicate slot submission, wrong participant, empty/oversize
  policy or intent field, wrong value, premature/late action, review before all
  intents, retry after settlement/refund, duplicate settlement/recovery,
  consuming unselected/out-of-order/already-consumed ticket, and zero/double
  withdrawal.

### Authorization

- Sponsor identity is `gl.message.sender_address` at creation.
- Participant slot is derived from exact locked addresses.
- Review is permissionless only after deterministic readiness.
- Recovery is sponsor-only.
- Ticket consumption is selected participant-only.
- Credit withdrawal is credit-owner-only by sender.

### Idempotency and double-action prevention

- Unique batch IDs and one immutable submission per slot.
- Append-only attempt count; review reads current attempt dynamically.
- Settlement status changes before credit creation can be repeated.
- Credit ledger debited before external transfer.
- Ticket consumed flag and canonical order prevent replay/out-of-order use.

## Write-method safety matrix

| Method | Caller | Allowed states | Forbidden states | Temporal/expiry gate | Idempotency | Value/accounting effect | Views affected | Negative tests |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `create_batch` | Any sponsor | Batch absent | Existing batch ID | `now < submit_deadline < review_deadline`; equality invalid | Duplicate ID rejects | Receives exactly 2 GEN; purse/received increase once | batch, accounting | empty/duplicate ID; duplicate participants; bad priority; empty/oversize policy; 0/1 GEN/over 2 GEN; deadlines at/past/reversed; non-payable metadata audit |
| `submit_intent` | Exact participant for derived slot | `OPEN`; own slot empty | READY, RETRYABLE, CLEARED, refunded; slot filled | `now < submit_deadline`; equality late even with stale OPEN | Second submission rejects | No GEN; submission count increases once | batch, intent | wrong caller; empty/oversize fields; deadline -1 succeeds, exact/+1 reject with state/accounting unchanged; duplicate; attached value rejects |
| `review_batch` | Any caller | READY or RETRYABLE; purse unsettled; 3 intents | OPEN, CLEARED, refunded | `now < review_deadline`; equality late even with stale READY/RETRYABLE | New append-only attempt only before terminal settlement | RETRYABLE moves no value; safe pair opens two 1 GEN credits and zeros purse; no safe pair opens 2 GEN sponsor credit and zeros purse | batch, attempts, relations, tickets, credits, accounting | incomplete; exact/+1 deadline; duplicate after terminal; malformed/extra/missing/duplicate/wrong-ID/wrong-orientation/cyclic graph; leader error; semantic disagreement; accounting unchanged on rejection/retry |
| `recover_incomplete` | Sponsor | OPEN; fewer than 3 intents; purse 2 GEN | READY/RETRYABLE/CLEARED/refunded; 3 intents | `now >= submit_deadline`; equality expired | One refund settlement; duplicate rejects | Opens 2 GEN sponsor credit and zeros purse | batch, credits, accounting | wrong caller; deadline -1; exact/+1; three intents; terminal/duplicate; unchanged accounting on rejection |
| `recover_unresolved` | Sponsor | READY or RETRYABLE; purse 2 GEN | OPEN, CLEARED, refunded | `now >= review_deadline`; equality expired | One refund settlement; duplicate rejects | Opens 2 GEN sponsor credit and zeros purse | batch, credits, accounting | wrong caller; deadline -1; exact/+1; terminal/duplicate; accounting unchanged on rejection |
| `consume_ticket` | Selected ticket participant | CLEARED; selected; correct next order; unconsumed | All non-CLEARED; unselected; out-of-order; consumed | N/A: finalized ticket order controls legality, not wall clock | Consumed once; duplicate rejects | No GEN; marks ticket consumed and advances consumed count | batch, ticket | wrong caller; unselected; order 2 before order 1; duplicate; refunded/retry state; accounting unchanged |
| `withdraw_credit` | Credit owner | Credit > 0 | Zero credit | N/A: pull-credit ownership/state controls legality | Debit before transfer; second call rejects | Decreases outstanding credit, increases withdrawn, emits exact EOA transfer | credit, accounting | zero credit; second withdrawal; transfer boundary; conservation after each selected/sponsor withdrawal |

No listed write may be implemented before its focused negative tests exist and
fail for the intended missing behavior.

## Evidence policy

- Authoritative sources: canonical contract state written by the locked sponsor
  and participant transaction senders.
- Provenance/authentication: deterministic sender/role verification plus exact
  binding to contract, batch, slot, revision, policy digest, and intent digest.
- Authorized attestor/signer: EVM-compatible transaction signer represented by
  `gl.message.sender_address`; the contract does not parse signature prose.
- Anti-replay event/digest identity: unique batch ID, fixed slot, revision 1,
  recomputed policy/intent digest, and current attempt ID.
- Signed timestamp bounds: transaction-time deadline checks; no offchain signed
  timestamp is accepted.
- Immutable policy/source version URLs and hashes: no external URL is authority;
  immutable onchain policy revision and digest are the version source.
- Allowed schemes/domains/paths: N/A; no web fetch.
- Time/window rules: exact entrypoint rules above.
- Size/count bounds: policy <= 4,000 ASCII characters; each action,
  precondition, and side-effect field <= 2,000 ASCII characters; exactly 3
  intents and exactly 3 pair results.
- Missing evidence: review rejects before nondeterminism while incomplete.
- Contradictory evidence: semantic relations may be incompatible; this is a
  valid meaning, not an authenticity failure.
- Unavailable source: N/A for remote source; runtime/model failure remains
  RETRYABLE and non-penalizing.
- Invalid/unverifiable attestation: revert before semantic review; no hard
  consequence or value movement.
- Canonical objective/policy source and hash: immutable `Batch.policy` and
  `policy_digest`.
- Workflow/entity, step/requirement, actor/subject binding: contract address,
  batch ID, slot, participant, revision, policy digest, and attempt ID.
- Prompt-injection boundary: policy and intent bodies are labeled untrusted
  contractual data. They cannot redefine IDs, authority, relation enums,
  pair coverage, priority, payees, amounts, tickets, or recovery.
- Private/unverifiable evidence excluded: all external facts and hidden context.

### Evidence Authority Matrix

| Consequential claim/fact | Evidence/artifact | Data controller | Authoritative source/issuer | Deterministic verification | Canonical objective/entity/actor binding | Freshness/anti-replay | Semantic role after verification | Non-penalizing failure state | Consequence blocked | Required negative test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Batch policy/roles/priority/deadlines govern clearing | Batch creation transaction and state | Sponsor controls creation bytes only | Exact sponsor sender and immutable contract state | Sender, distinct participants, unique priority permutation, bounded ASCII policy, exactly 2 GEN, ordered future deadlines | Network, contract, batch, sponsor, participants, policy revision/digest | Unique batch ID; frozen after creation | Defines comparison policy and deterministic tie-break | Revert before creation | Submission, review, tickets, credits | Correct digest from wrong sponsor/batch or duplicate participant leaves state/accounting unchanged |
| Intent belongs to one locked participant/slot | Intent submission transaction and state | Named participant controls its own bytes | Exact participant sender | Recomputed digest, sender/slot/revision, ASCII/size, one submission | Contract, batch, participant, slot, policy digest, revision | Before deadline; slot/revision unique | Supplies only bounded semantic action data | Revert; no attempt or consequence | Pair graph, selection, ticket, credit | Hash-valid bytes from wrong actor/batch/slot/revision leave count/purse unchanged |
| Normalized graph covers exact current intent set | Leader result plus validator independent replay | Leader proposes; validators re-evaluate | GenLayer semantic consensus over captured canonical inputs | Exactly three canonical pairs; exact IDs; unique coverage; allowed relations; orientation normalization; cycle and consequence invariants | Batch, policy digest, intent-set digest, attempt ID, exact intent IDs | Current attempt in READY/RETRYABLE only | Classifies relations only; contract derives pair/order/payees/amounts | Revert or RETRYABLE; no tickets/credits/value movement | Selection, tickets, settlement, credit, refund | Shape-valid wrong/missing/extra/duplicate/misoriented/cyclic graph leaves all hard state/accounting unchanged |

## Consensus design

### Leader task

- Inputs: captured immutable batch policy, fixed priority, and exact three
  intents with IDs/authors/actions/preconditions/side effects.
- Fetch: none; exact canonical state is captured before nondeterminism.
- Extraction: model evaluates each of the three canonical unordered pairs.
- Normalization: fixed intent orientation, allowed relation enum, exact pair ID,
  unique pair coverage, bounded relation basis code.
- Structured output: `coverage`, `batch_id`, `attempt_id`, `policy_digest`,
  `intent_set_digest`, and exactly three pair records.

### Consensus-critical fields

| Field | Type/bounds | Comparison rule | Why critical |
| --- | --- | --- | --- |
| `batch_id`, `attempt_id` | Exact stored IDs | Exact equality | Prevent cross-batch/attempt replay |
| `policy_digest`, `intent_set_digest` | Fixed lowercase hex digest | Exact equality | Bind result to exact canonical inputs |
| `coverage` | `COMPLETE` or `RETRYABLE` | Exact equality | Hard consequence requires complete evidence |
| Pair ID set | Exactly 3 unique canonical pair IDs | Exact set equality | Prevent missing/extra/duplicate intents |
| Relation per pair | `INDEPENDENT`, `LEFT_BEFORE_RIGHT`, `RIGHT_BEFORE_LEFT`, `INCOMPATIBLE` | Exact semantic equality after canonical orientation | This is the judgment that controls selection/order |
| Basis code per pair | Bounded locked enum | Exact equality | Prevent unsupported reasoning from silently authorizing tickets |
| Rationale | Bounded text | Ignored for consensus and settlement | Wording may vary without changing meaning |

### Validator

- Independent evidence/replay: re-run the same bounded semantic task over exact
  captured inputs; never validate leader shape alone.
- Semantic rule: every normalized pair relation, coverage field, and binding
  must match. Different relation meaning returns `False`.
- Rejection conditions: leader not `gl.vm.Return`; wrong bindings; incomplete,
  extra, missing, duplicated, invalid, or semantically different pair graph;
  invalid basis; cyclic order constraints; parser/model error.
- `UNDETERMINED` handling: no terminal `UNDETERMINED`; safe normalized
  `RETRYABLE` stores only append-only attempt metadata and moves no value or
  rights. Consensus failure reverts entirely.

### Rationale policy

Rationale is bounded diagnostic text only. It cannot define authority,
relations, IDs, payees, amounts, selection, order, tickets, refunds, or policy.

## Deterministic settlement invariants

- Coverage is `COMPLETE` before consequence.
- Expected intent IDs A/B/C each occur in exactly two pair records.
- Exactly three canonical unordered pair IDs occur once each.
- No extra/missing/duplicate ID or invalid relation/basis is accepted.
- Directed order relations form no two-node contradiction or three-node cycle.
- Candidate pairs marked `INCOMPATIBLE` are never selected.
- The selected pair is derived by contract code: highest locked-priority
  compatible pair; ties resolve by canonical pair ID.
- Canonical order is derived from relation; independent pairs use locked
  priority then canonical ID.
- Selected payees are exact authors of selected intents; model cannot supply
  addresses.
- Each selected credit is exactly 1 GEN; sum is exactly 2 GEN. No rounding or
  remainder exists.
- No-compatible-pair result credits exactly 2 GEN to sponsor.
- Purse becomes zero exactly once when credits are created.

## Consequence and accounting

| Verdict/outcome | Canonical state change | Consumer action | Value movement |
| --- | --- | --- | --- |
| Complete graph with compatible pair | `CLEARED`; exact relations stored; two ordered tickets granted | Consumer reads/participant consumes order 1 then 2 | 1 GEN credit to each selected participant |
| Complete graph with no compatible pair | `NO_PAIR_REFUNDED`; no tickets | No execution authorized | 2 GEN sponsor credit |
| Safe `RETRYABLE` | Attempt appended; batch remains retryable; no tickets | Retry before review deadline | None; 2 GEN remains locked |
| Incomplete after submit deadline | `INCOMPLETE_REFUNDED` | No execution authorized | 2 GEN sponsor credit |
| Ready/retryable after review deadline | `UNRESOLVED_REFUNDED` | No execution authorized | 2 GEN sponsor credit |

- Accepted/finalized boundary: contract state consequence is part of the
  accepted execution; public evidence waits for `FINALIZED` and successful
  execution result before claiming it.
- Ledger invariant: `total_received = purse_locked + outstanding_credits + total_withdrawn`.
- Child-message/transfer evidence: withdrawal debits ledger first and emits an
  EOA transfer; evidence binds parent/child outcome and destination balance.
- Withdrawal/settlement: pull credits only; one settlement and one withdrawal
  per credited balance.
- Cure/appeal/restore: no appeal/cure in v1. Retry is allowed only for RETRYABLE
  before review deadline; terminal outcomes are immutable.

### Value-destination matrix

| Value item | Payer/source | Locked state | Release destination | Refund destination | Forfeit destination | Terminal states covered | Duplicate/late/retry behavior | Canonical proof view |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 GEN coordination purse | Sponsor `create_batch` | OPEN, READY, RETRYABLE | 1 GEN to each of two selected-participant credits on CLEARED | 2 GEN sponsor credit on NO_PAIR_REFUNDED, INCOMPLETE_REFUNDED, UNRESOLVED_REFUNDED | None | All terminal/refund states | Settlement once; retries move no value; late recover follows exact guards; duplicate rejects | `get_batch`, `get_accounting`, `get_credit` |
| Selected participant credit | Settled purse ledger | CLEARED until withdrawal | Exact selected participant EOA | N/A | None | withdrawn/unwithdrawn credit | Debit before transfer; second withdrawal rejects | `get_credit`, `get_accounting`, receipt/balance evidence |
| Sponsor refund credit | Settled purse ledger | Refund state until withdrawal | Exact sponsor EOA | N/A | None | all three refund outcomes | Debit before transfer; second withdrawal rejects | `get_credit`, `get_accounting`, receipt/balance evidence |

No purse, credit, or ticket depends on a later voluntary actor action for its
eventual recoverability: sponsor expiry recovery handles incomplete/unresolved
batches, and every credit has a pull withdrawal.

## Reusable interface

### Write methods

- `create_batch(batch_id, participant_a, participant_b, participant_c,
  priority_csv, policy, submit_deadline, review_deadline)` payable exactly 2 GEN.
- `submit_intent(batch_id, action, preconditions, side_effects)`.
- `review_batch(batch_id)`.
- `recover_incomplete(batch_id)`.
- `recover_unresolved(batch_id)`.
- `consume_ticket(batch_id, intent_id)`.
- `withdraw_credit()`.

### View methods

- `get_batch(batch_id)`.
- `get_intent(batch_id, intent_id)`.
- `get_attempt(batch_id, attempt_number)`.
- `get_pair_relation(batch_id, left_intent_id, right_intent_id)`.
- `get_ticket(batch_id, intent_id)`.
- `get_credit(account)`.
- `get_accounting(batch_id)`.

### Consumer/callback

- Authentication: no callback in v1. Consumers read finalized tickets; the
  selected participant consumes its own ticket in canonical order.
- Idempotency key: `batch_id + intent_id`; consumed once.
- Failure/retry: an external consumer failure cannot alter contract accounting;
  ticket remains canonical until selected participant consumes it.
- Authorized cancellation: none after CLEARED; pre-terminal recovery follows
  sponsor/time/state rules only.

## Threat model

| Threat | Attack | Mitigation | Test |
| --- | --- | --- | --- |
| Sponsor role manipulation | Duplicate participants or priority values | Deterministic distinct-address and permutation validation | create rejects with state/value unchanged |
| Wrong actor provenance | Actor submits another slot's hash-valid bytes | Sender-to-slot derivation and immutable binding | wrong actor/batch/slot/revision tripwires |
| Prompt injection | Intent text tells model to pick a payee/change policy | Prompt labels bodies untrusted; locked enums/bindings; contract derives consequence | injected authority/payout text cannot affect graph bindings/accounting |
| Malicious leader shape-valid graph | Missing/extra/duplicate/wrong ID or relation | Exact-set settlement invariants before mutation | each invalid semantic shape rejected |
| Semantic disagreement | Leader and validator choose different relation | Custom validator exact meaning comparison | validator unit/replay tests return false |
| Order cycle | Three directed relations create a cycle | Deterministic cycle check before selection | cyclic graph rejected with unchanged state/value |
| Late action under stale phase | Submit/review after deadline while status remains OPEN/READY | Entrypoint-local clock guard | deadline -1/equality/+1 with stale status |
| Premature malicious recovery | Wrong caller or pre-deadline refund | Sponsor/state/time/interest guards | wrong caller, pre-boundary, terminal, duplicate tests |
| Double settlement/withdrawal | Re-review terminal batch or withdraw twice | Terminal status and debit-before-transfer | duplicate review/recovery/withdraw tests |
| Out-of-order ticket use | Consume second ticket first | `next_ticket_order` invariant | order-2-first rejects |

## Test plan

- Happy path: create with 2 GEN; submit three intents; complete mixed
  independent/ordered graph; selected pair, order, tickets, credits, consume,
  two withdrawals, zero accounting.
- Unauthorized: wrong participant submit; wrong sponsor recovery; wrong ticket
  consumer.
- Isolation: two batches with different participants/policies/credits never
  overwrite one another.
- Evidence failure: wrong batch/slot/revision/digest/intent-set/policy bindings.
- Malicious leader: not Return, invalid enum/basis, wrong IDs, extra/missing/
  duplicate pairs, cyclic graph, model-selected address/amount ignored/rejected.
- Prompt injection: intent attempts to redefine authority, success, priority,
  payout, destination, IDs, relation enum, or policy.
- Semantic mismatch: same shape but validator relation differs.
- Verdict classes: independent, both order directions, incompatible, no safe
  pair, retryable.
- Duplicate: batch, submission, terminal review, recovery, ticket consumption,
  withdrawal.
- Recovery/value write safety: every safety-row negative case, terminal state,
  and conservation invariant.
- Accounting/value: exact 2 GEN input; two 1 GEN credits or one 2 GEN sponsor
  refund; no residual; debit-before-transfer.
- Temporal: every deadline at -1, equality, +1 with stale phase and unchanged
  state/accounting after rejection.
- Consumer enforcement: order 2 cannot consume before order 1; only selected
  authors consume.
- Undetermined/retry: RETRYABLE moves no GEN/ticket; current attempt is read
  dynamically; expiry refund closes liability.
- Metadata/deployment: ASCII/header/class checks, payable metadata, raw and
  normalized receipt parser fixtures, safe-field projection.

## Claim-to-code matrix

| Product claim | Contract method/state | View/read | Direct test | Network evidence |
| --- | --- | --- | --- | --- |
| Exact 2 GEN sponsor purse funds a batch | `create_batch`, Batch purse/received | batch/accounting | exact/wrong value and payable metadata | finalized create receipt + accounting read |
| Only three named actors author immutable intents | `submit_intent`, Intent | intent/batch | sender/slot/duplicate/binding/isolation | three finalized submits + intent reads |
| Validators agree on meaning, not JSON shape | `review_batch` custom validator | attempts/relations | validator agreement/disagreement and malicious shape-valid graphs | successful review result + exact graph reads |
| Complete graph controls deterministic pair/order | settlement invariant and selection helper | relations/tickets | complete/missing/extra/cycle/priority cases | finalized selected IDs/order/tickets |
| Selected intents receive fixed rights and credits | CLEARED tickets/credit ledger | tickets/credit/accounting | exact authors, 1 GEN each, no model payees | canonical tickets/credits after finality |
| No pair or expiry refunds sponsor | review/recover methods | batch/credit/accounting | no-pair, incomplete, unresolved boundaries | refund lifecycle on a separate batch if bounded budget permits; otherwise marked pending |
| Tickets are one-time and ordered | `consume_ticket` | ticket/batch | wrong actor, order 2 first, duplicate | two finalized consume calls + ticket reads |
| Credits withdraw once with conservation | `withdraw_credit` | credit/accounting | zero/double withdraw, debit first, conservation | receipts + allowlisted child result/balance delta + zero accounting |
| No app/Vercel is part of contribution | repository tree | Git tree | public allowlist audit | public GitHub tree only |

## Analogue and differentiation matrix

| Analogue/prior idea | Similar dimensions | Structural difference | Collision decision |
| --- | --- | --- | --- |
| SkillSlot Clearing | Agents, compatibility, allocation rights | Offer/request graph and delivery escrow versus pairwise action-conflict graph and ordered tickets | Not duplicate |
| SemanticPolicyQuorum | Natural-language constraints and execution authorization | Many policies authorize one plan versus three competing intents clear two slots | Not duplicate |
| TraceSettle | Multi-agent entities, classification, credits | Post-hoc causal fault DAG versus pre-execution conflict/order graph | Not duplicate |
| CanonMerge | Semantic coexistence and two rights | Two creative branches merge/fork content graph versus choose two of three operational intents | Not duplicate |
| MissionMesh | Multi-agent scheduling/assignment | Decomposes missions and reviews delivery versus fixed intent concurrency clearing | Not duplicate |
| Internet Court | Adversaries, semantic jury, escrow | Generic bilateral claim dispute versus exact complete multi-intent relation graph and deterministic scheduling consequence | Not duplicate |
| Legacy SubjectiveVoteResolver | LLM chooses a winner | ConcordBatch has authenticated inputs, exact coverage, graph invariants, rights, recovery, and accounting | Exclusion avoided |

## Deployment and evidence plan

- Network: Studio Dev chain 61997 only.
- Actors/wallet separation: use authorized existing EOAs when sufficient; never
  print keys. New/funding actions require explicit action-time authorization.
- Deploy steps: verify CLI network/RPC/chain; lint/tests/check; fee profile or
  estimate as required by v0.6; deploy exact source; verify successful execution,
  schema, class, source identity, and explorer address/tx.
- Consequential lifecycle: create with 2 GEN; three role-authenticated intents;
  semantic review; read graph/order/tickets/credits; consume order 1/2; withdraw
  both 1 GEN credits; read zero locked/outstanding accounting.
- Canonical reads: all views in the claim-to-code matrix.
- Balance/receipt proof: allowlisted tx hash/status/execution result, sender,
  recipient, value in GEN, selected state IDs, and before/after public balances;
  never raw receipt/node config.
- Evidence path: `docs/evidence/studio-dev/` only.
- Resume/idempotency: active `deployment.json` binds network, chain, source
  commit, runner/API unit, address, txs, batch/attempt IDs; mismatches force a
  revision rollover, not blind replay.

## Definition of Done

### Intelligent Contracts

- [x] Reusable primitive with three named consumers.
- [x] Semantic validator judgment over complete pair meaning.
- [x] Direct execution-right and GEN-credit/refund consequence.
- [x] Documented views/ticket adapter as reuse proof; no pass-through consumer.
- [x] Adversarial direct and validator-replay tests.
- [x] Real Studio Dev lifecycle with successful execution results.
- [x] Canonical graph/ticket/credit/accounting evidence and explorer URLs.
- [x] Contract-only public Git repository with meaningful history and passing CI.
- [x] `Project concord-batch -Category intelligent-contracts -ExplorerUrl
  https://explorer-studio-dev.genlayer.com/address/0x678607d653706E1Bd4B0812035e5b4bE661438bc`
  reports `NO BLOCKER`.

## Honest limitations

- V1 is exactly three participants and two execution slots.
- Studio Dev revision `0xcDe034a36873C39eCf4e268f256Bf2f46A2fe029`
  is superseded and abandoned: its prompt omitted exact canonical intent and
  pair IDs, two live reviews safely resolved to RETRYABLE, and its 2 GEN purse
  remains locked. No further value will be sent to that revision. The active
  replacement must prove a terminal lifecycle independently.
- Studio Dev revision `0xAccF5A83F41ea684b563B6D569cc331E56fDa0dB`
  is also superseded and abandoned after one safe RETRYABLE result exposed a
  second normalization bug: contract-derived `basis` was incorrectly fed back
  through the strict model-output normalizer. Its 2 GEN purse remains locked;
  it receives no further value.
- It judges declared intent meaning, not actual external side effects or
  execution completion.
- Validators decide only the four-class pair relation. Contract code derives
  the stored basis enum from that relation; model prose cannot select or add a
  settlement field.
- Priority is sponsor-locked and transparent, not socially neutral or globally
  optimal; participants accept it by submitting.
- No callback, frontend, Vercel, external adopter, legal guarantee, Portal
  acceptance, or multi-network evidence is claimed.
- The one-model design spike is not validator consensus evidence.

## Kill criteria

- The semantic graph cannot be made stable at pair-relation meaning level.
- Validators can disagree on a relation while both pass.
- Current GenVM cannot validate the exact v0.3 runner/API unit.
- A hard consequence can occur with incomplete/wrong provenance or graph
  coverage.
- Any terminal/recovery branch can orphan the 2 GEN purse or duplicate credit.
- Collision review finds an existing complete semantic conflict-graph clearing
  primitive matching four or more fingerprint dimensions.
