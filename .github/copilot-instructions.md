**Repository Overview**

This repository is a small Bronze-layer ingestor for a data engineering exercise. The core job is to scan `landing/`, classify incoming files and move them into `bronze/` (valid) or `bad_data/` (empty/corrupt). The single runnable entry is `ingestor.py`.

**How to run (developer workflow)**

- **Run from project root**: `python ingestor.py` (no external deps; uses stdlib).
- Ensure the three folders exist at project root: `landing/`, `bronze/`, `bad_data/`. If any folder is missing the script logs an error and exits.

**Key files & locations**

- `ingestor.py` — main pipeline script; implements scanning, classification, moving, and summary logging.
- `landing/` — incoming raw files (examples: `landing/data_batch_20251222_090537_99.json`).
- `bronze/` — destination for files with content (> 0 bytes).
- `bad_data/` — destination for files with 0 bytes or that produced I/O errors.
- `README.md` — describes the exercise and explicit functional requirements.

**Important behavioral patterns (do not change without checking tests/README)**

- Path handling: the code uses `Path.cwd()` as the base. Always run the script with current working directory set to the repository root so paths resolve as expected.
- File classification rule: `st_size > 0` => move to `bronze/`; `st_size == 0` => move to `bad_data/`.
- Moving files: implemented with `shutil.move(...)` (preserves filename). Keep using `shutil` rather than reimplementing copy+delete unless necessary.
- Error handling: `ingestor.py` intentionally catches all exceptions per-file and continues processing. Preserve this robustness when modifying processing logic.
- Logging: lightweight `logging` to stdout is relied on for visibility and simple QA. Keep the `INFO`-level summary at the end (counts and whether `landing/` is empty).

**Naming conventions & data cues**

- Incoming filenames follow `data_batch_YYYYMMDD_HHMMSS_NN.ext` and include `.json`, `.csv`, `.xml` variants. Parsers (if added) should use the extension to pick the correct reader.

**Common changes you might implement (and where to start)**

- Add parsers or validators: create a new module (e.g., `parsers.py`) and call from `ingestor.py` in the try/except block so bad files are quarantined without breaking the loop.
- Add unit tests: focus on small functions (e.g., a new `classify_file(path)` function) and mock `shutil.move` and filesystem using `tmp_path` fixtures.

**Pitfalls & gotchas discovered in the codebase**

- Running the script from a different CWD will make `Path.cwd()` point elsewhere — tests or CI should `chdir` into project root or update code to use `Path(__file__).parent` if relative imports are required.
- There is no `requirements.txt`; the script uses only stdlib. If you add third-party packages, update `requirements.txt`.

**What an AI-code assistant should do first**

- Read `ingestor.py` to understand the single-file control flow (scan -> classify -> move -> summary).
- Verify `landing/`, `bronze/`, `bad_data/` presence before changing behavior.
- Preserve the per-file `try/except` behavior and final summary logging when refactoring.

**Example concrete edits**

- Small refactor: extract the file-classification logic into `ingestor.classify_file(path)` and add unit tests that assert moves and counters using temporary directories.
- Add an integration script: a `run.sh`/`run.ps1` wrapper that ensures CWD is repository root and then runs `python ingestor.py`.

If any section is unclear or you want more detail (example unit tests, CI steps, or a suggested `requirements.txt`), tell me which part to expand or adjust.
