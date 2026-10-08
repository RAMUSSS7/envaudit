# envaudit

Keep your `.env` and `.env.example` files in sync, and make sure `.env` never gets committed by accident.

Zero dependencies. Python 3.9+.

## Why?

Add a new variable to `.env`, forget to add it to `.env.example`, and your teammate's app breaks. Forget to git-ignore `.env`, and your secrets end up on GitHub. `envaudit` catches both in one command.

## Install

```bash
pip install git+https://github.com/RAMUSSS7/envaudit.git
```

## Usage

Run it from your project folder:

```bash
envaudit check
```

Example output:

```
[ERROR] DATABASE_URL is in .env but missing from .env.example
[ERROR] NEW_KEY is in .env.example but missing from .env
[ERROR] .env is not ignored by .gitignore (your secrets could be committed!)
```

When everything is fine:

```
[OK] .env and .env.example are in sync.
```

### Options

| Option | Default | Meaning |
|---|---|---|
| `--env` | `.env` | path to your real env file |
| `--example` | `.env.example` | path to the template file |
| `--gitignore` | `.gitignore` | path to your .gitignore |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | all good |
| 1 | problems found |
| 2 | a file was not found |

This makes it easy to use in CI or as a pre-commit hook.

## What it checks

- Keys present in `.env` but missing from `.env.example`
- Keys present in `.env.example` but missing from `.env`
- Whether `.env` is covered by `.gitignore`

Only key names are compared. Values are never printed.

## Development

```bash
python -m unittest discover -s tests -t . -v
```

## Roadmap

- [ ] Detect unused / undefined variables by scanning source code
- [ ] Detect common secret patterns (AWS, GitHub, Stripe keys)
- [ ] Publish to PyPI

## License

MIT
