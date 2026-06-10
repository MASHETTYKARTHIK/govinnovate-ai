# Compliance & CI Fix Plan (GovInnovate AI)

## Step 1: Make project description detectable
- [ ] Update README description section and add a dedicated `PROJECT_DESCRIPTION.md` file.

## Step 2: Make Git tags/release detectable
- [ ] Create a git tag (`v1.0.0`) and push it to remote.

## Step 3: Ensure coverage + reports are stable for CI
- [ ] Verify `.gitlab-ci.yml` artifacts include `coverage.xml` and job names match expected checker patterns.

## Step 4: Run checks locally before final commit
- [ ] `pre-commit run -a`
- [ ] `ruff check .`
- [ ] `python -m mypy .`
- [ ] `pytest -q`
- [ ] `pytest --cov=backend --cov=streamlit_app --cov-report=xml:coverage.xml`

## Step 5: Commit strategy
- [ ] Create multiple commits: one per major step (description, CI/report stabilization, tag creation).


