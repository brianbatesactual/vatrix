# Vatrix Feature → Release Workflow

This checklist outlines the full process for developing a new feature and publishing it to PyPI from a protected `main` branch using GitHub, `make`, and `twine`.

---

## ✅ 1. Create Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/<short-description>
```

---

## ✍️ 2. Develop the Feature

- Write or refactor code under `src/vatrix/`
- Add or update tests in `tests/`
- Document the feature in `docs/` and update `mkdocs.yml`
- Bump version in `pyproject.toml` (e.g., `version = "0.2.1"`)

---

## 🧪 3. Format, Lint, Test

```bash
make format     # black + isort
make lint       # flake8
make check      # pre-commit + lint + format
make test       # pytest
```

---

## 📦 4. Build & Upload to TestPyPI

```bash
make freeze          # update requirements.txt
make test-release    # build and upload to TestPyPI
```

Install test release:
```bash
pip install --index-url https://test.pypi.org/simple vatrix
```

---

## 📥 5. Commit Changes

```bash
git add .
git commit -m "✨ Add <feature>: <summary>"
git push origin feature/<short-description>
```

---

## 🚀 6. Create Pull Request

- Open a PR from `feature/branch` → `main`
- Include:
  - Summary of changes
  - Feature usage or testing notes
  - Optional: "Closes #issue"

---

## ✅ 7. Merge PR

- Approve PR (or request review)
- Squash and merge via GitHub UI
- Pull latest `main`:

```bash
git checkout main
git pull origin main
```

---

## 🏷️ 8. Tag the Release

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z: <highlights>"
git push origin vX.Y.Z
```

---

## 📦 9. Publish to PyPI

```bash
make release
```

Or manually:
```bash
python3 -m build
twine upload dist/*
```

---

## 📑 10. Update GitHub Release Notes

- Go to GitHub → Releases
- Find the new tag
- Click "Edit" to:
  - Add highlights
  - Note features / fixes / breaking changes

---

## 💡 Optional Enhancements

- Update `docs/changelog.md`
- Publish docs via `mkdocs gh-deploy`
- Announce release on README, social, or blog

---

## ⌛ Example Versioning Conventions

| Type       | Version Bump | Example      |
|------------|---------------|--------------|
| Patch fix  | x.y.Z → x.y.Z+1 | `0.2.1 → 0.2.2` |
| New feat   | x.y.Z → x.y+1.0 | `0.2.1 → 0.3.0` |
| Breaking   | x.y.Z → x+1.0.0 | `0.2.1 → 1.0.0` |

