## Cursor Cloud specific instructions

This is a pure-Python CLI application ("Kiki's Delivery Service") with **zero external dependencies**. It uses only the Python standard library.

### Running

- **Run the app:** `python3 main.py` (interactive) or `echo "file" | python3 main.py` (from sample input file at `import/sample_input.txt`).
- **Run tests:** `python3 -m unittest discover tests -v`
- See `README.md` for full usage details and project structure.

### Notes

- No package manager, no `requirements.txt`, no build step. Python 3.7+ is the only prerequisite.
- The `python` alias may not be available; always use `python3`.
