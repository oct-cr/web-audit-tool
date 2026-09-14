- ensure the workspace virtualenv is created and activated before running or debugging in new terminals.
- separate model and view logic
- prefer composition over inheritance
- write pure functions when possible
- never write explanatory implementation comments. Only acceptable comments are short explanations for hardcoded values (e.g., chars, colors). Prefer clear, self-explanatory code.
- use type hints for all functions and methods
- use Ruff for rapid diagnosis

- when asked with "check" fix issues in the codebase by running `source .venv/bin/activate && make check` and addressing any problems that arise.
- when asked with "debug" run the Debug named Task in the VSCode debugger and address any issues that arise.