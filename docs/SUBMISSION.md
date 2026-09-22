# Portal submission fields

- Title: `ConcordBatch`
- Category: `Intelligent Contracts`
- Description character count: `768`
- Evidence URL: `https://github.com/duclucky/concord-batch`
- Contract Address: `0x678607d653706E1Bd4B0812035e5b4bE661438bc`
- Explorer Deploy Tx URL: `https://explorer-studio-dev.genlayer.com/tx/0xedc894e3e468dafb3d1c17b8f17969b1d86e10442478fb82b29e057d6f9c0231`
- Network: `Studio Dev (chain ID 61997)`

## Description

ConcordBatch is a reusable GenLayer Intelligent Contract that clears two compatible action intents from three wallet-authenticated participants, then grants ordered one-time tickets and fixed GEN credits. GenLayer validators independently classify the complete pairwise conflict/order graph and agree on the meaning of every relation, not JSON wording or format; contract code validates exact coverage, rejects cycles, and deterministically selects the consequence. A2A tool gateways, DAO automation queues, and turn-based AI games can reuse its canonical tickets and accounting views. It includes adversarial direct-mode tests, deployment parsers, full safety/evidence documentation, and a verified Studio Dev deployment at 0x678607d653706E1Bd4B0812035e5b4bE661438bc.

## Worked lifecycle

Real Studio Dev batch `concord-demo-479caf0` received exactly 2 GEN. Validators
classified A/B as incompatible and A/C plus B/C as independent. Locked priority
selected A then C. The finalized state is `CLEARED`; A and C each have 1 GEN
credit; locked value is 0 GEN. Canonical accounting reads 2 GEN received, 0 GEN
locked, 2 GEN credits, and 0 GEN withdrawn.

The Portal Evidence field takes the GitHub repository URL. The owner submits
this on `portal.genlayer.foundation` under Builder -> Intelligent Contracts and
ticks the reCAPTCHA; this repository does not claim submission or acceptance.
