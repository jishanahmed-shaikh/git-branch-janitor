# git-branch-janitor

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/jishanahmed-shaikh/git-branch-janitor/actions/workflows/ci.yml/badge.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

**Keep your local git environment clean by deleting branches already merged into main.**

Over time, local branches pile up — feature branches, hotfixes, experiments. `git-branch-janitor` finds every branch that's been merged and wipes them out in one shot, with a dry-run mode so you always know what's going to happen before it does.

---

## Install

```bash
pip install git-branch-janitor
```

From source:

```bash
git clone https://github.com/jishanahmed-shaikh/git-branch-janitor.git
cd git-branch-janitor
pip install -e .
```

---

## Usage

```bash
# Preview what would be deleted (safe, no changes)
git-janitor --dry-run

# Delete merged branches interactively
git-janitor

# Delete without confirmation prompt
git-janitor --yes

# Check against a different base branch
git-janitor --base develop

# Show version
git-janitor --version
```

### Example Output

```
🌿 Merged branches (base: main):

   feature/login-page
   fix/typo-in-readme
   chore/update-deps

Delete 3 branch(es)? [y/N] y

  🗑️  Deleted branch 'feature/login-page'
  🗑️  Deleted branch 'fix/typo-in-readme'
  🗑️  Deleted branch 'chore/update-deps'

  Done. 3 deleted, 0 failed.
```

---

## Protected Branches

The following branches are **never** deleted, regardless of merge status:

`main` · `master` · `develop` · `dev` · `staging` · `production`

The currently active branch is also always skipped.

---

## Flags

| Flag | Description |
|------|-------------|
| `--base <branch>` | Base branch to check merges against (default: `main`) |
| `--dry-run` | Show what would be deleted without making changes |
| `--yes` | Skip confirmation prompt |
| `--version` | Show version and exit |

---

## How It Works

1. Runs `git branch --merged <base>` to find all merged local branches
2. Filters out protected branch names and the current active branch
3. Shows the list and asks for confirmation (unless `--yes`)
4. Deletes each branch using `git branch -d` (safe delete — won't remove unmerged work)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) — © 2026 Jishanahmed AR Shaikh
