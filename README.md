# task-cli

A tiny, dependency-free command-line to-do manager written in Python. Tasks are stored in `~/.tasks.json` (override with the `TASKS_FILE` env var).

## Usage

```bash
python tasks.py add Buy milk
python tasks.py list
python tasks.py done 1
python tasks.py list --all
python tasks.py rm 1
```

## Tests

```bash
python -m unittest
```

## Ideas to extend

- Due dates and priorities
- Tags and filtering
- Colored output

## License

MIT
