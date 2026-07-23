# requirements.txt — Overview

The `requirements.txt` file lists all Python packages required to run this project. It was generated using:

```bash
pip freeze > requirements.txt
```

## How it integrates in this lab

- **Installation** — When setting up the project without Pipenv, install all dependencies in one command:
  ```bash
  pip install -r requirements.txt
  ```
- **Consistency** — Ensures every developer and environment uses the exact same package versions, preventing version mismatch errors.
- **CI/CD** — Automated pipelines (e.g. GitHub Actions) use `requirements.txt` to install dependencies before running tests.
- **Deployment** — Hosting platforms like Render or Heroku automatically detect and install from `requirements.txt` during the build step.
- **Updating** — After installing a new package, regenerate the file with `pip freeze > requirements.txt` and commit the changes.
