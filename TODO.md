# TODO — Final compliance + pipeline stability

- [ ] Inspect compliance checker expectations (heuristics) by validating local tooling outputs.
- [ ] Update `.pre-commit-config.yaml` to ensure type-check (mypy) and security hooks are clearly detectable.
- [ ] Update `.gitlab-ci.yml` job scripts/artifact/report filenames to match checker expectations.
- [ ] Run local validations: `black --check .`, `ruff check .`, `python -m mypy .`, `pytest -q`, and coverage XML generation.
- [ ] Create branch `blackboxai/final-compliance-fixes`, commit, and push.
- [ ] (Optional) Open MR to `main` if MR not already created.
