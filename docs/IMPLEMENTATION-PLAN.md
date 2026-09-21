# ConcordBatch implementation plan

1. Lock the current v0.3 runner/header/import unit with official SDK evidence,
   installed `genvm-lint`, and one minimal local semantic-lint spike.
2. Add test harness/config and failing tests for storage, creation, exact 2 GEN,
   role authorization, isolation, deadlines, recovery, settlement invariants,
   tickets, credits, and withdrawals.
3. Implement one ASCII-only `ConcordBatch` contract from the specification,
   keeping every nondeterministic operation inside sandboxed
   `gl.vm.run_nondet_default` and comparing the complete graph meaning.
4. Add validator-replay tests, AST/header/payability checks, and raw/normalized
   receipt parser fixtures; make `npm run check` the full local gate.
5. Run deploy-clean scans, semantic lint, direct tests, and a bounded exact-source
   Studio Dev smoke before the value lifecycle.
6. Create resumable safe-field deployment/lifecycle tooling, deploy with the
   authorized account, execute the 2 GEN lifecycle, and store canonical evidence.
7. Review source/spec/claims, create meaningful commits, audit the exact public
   allowlist, publish GitHub, verify CI and URLs, then generate Portal fields and
   run the required zero-blocker precheck.

Every task uses its specification acceptance cases. A failed gate or unsafe API
drift stops execution; tests/checkers are never weakened to obtain a pass.

