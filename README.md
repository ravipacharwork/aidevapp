# aidevapp

A simple web application with a welcome page and a contact form, plus a
GitHub Actions workflow that runs basic code quality checks.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Landing page: welcome message + contact form |
| `scripts/check_quality.py` | Static quality checker (structure, tags, hygiene) |
| `.github/workflows/code-quality.yml` | CI workflow running the checks |

## Run locally

Open `index.html` in any browser — no build step or dependencies.

Run the quality checks with:

```bash
python3 scripts/check_quality.py
```

## What the checks verify

- Required HTML structure (`doctype`, `html`, `head`, `body`)
- Responsive viewport meta tag and a page `<title>`
- Contact form present with `name`, `email` and `message` fields
- Balanced opening/closing tags
- No overly long lines, trailing whitespace or tab characters

## CI

The workflow runs on every push and pull request to `main`, and can also be
started manually from the **Actions** tab (`workflow_dispatch`).
