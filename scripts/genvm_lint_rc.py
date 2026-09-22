"""Compatibility entrypoint for the pinned GenVM v0.3 semantic linter.

genvm-linter 0.11.1-rc.2 validates the v0.3 SDK but its reachability table can
omit the renamed sandboxed custom-validator entrypoint on Linux. Extend only
that table without changing any contract rule or installed package.
"""

from genvm_linter.lint import safety


safety.SafeEntryPointFinder.SAFE_PATTERNS["gl.vm.run_nondet_default"] = [0, 1]
safety.NONDET_SPAWN_CALLS = safety.NONDET_SPAWN_CALLS | {"gl.vm.run_nondet_default"}

from genvm_linter.cli import main


if __name__ == "__main__":
    main()
