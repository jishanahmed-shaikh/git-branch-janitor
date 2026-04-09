# git-branch-janitor

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-Integration-F05032?style=flat&logo=git&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)
![CLI](https://img.shields.io/badge/Tool-CLI-orange?style=flat)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat)

Local branches pile up fast. `git-branch-janitor` finds every branch already merged into main and cleans them up in one command. Dry-run first, delete when ready.

---

## Quick Start

```bash
pip install git-branch-janitor
```

```bash
# See what would be deleted before touching anything
git-janitor --dry-run

# Clean up with a confirmation prompt
git-janitor

# Skip the prompt and just do it
git-janitor --yes
```

---

## All Flags

| Flag | What it does |
|------|--------------|
| `--base <branch>` | Branch to check merges against (default: `main`) |
| `--dry-run` | Preview deletions without making any changes |
| `--yes` | Skip the confirmation prompt |
| `--version` | Print version and exit |

---

## Example Run

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

These are never touched, no matter what:

`main` `master` `develop` `dev` `staging` `production`

Your currently active branch is also always skipped.

---

## Under the Hood

Runs `git branch --merged <base>` to get the list, filters out protected names and the active branch, then deletes each one using `git branch -d` (safe delete, will not remove unmerged work).

No external dependencies. Pure Python + subprocess.

---

## Install from Source

```bash
git clone https://github.com/jishanahmed-shaikh/git-branch-janitor.git
cd git-branch-janitor
pip install -e .
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © 2026 Jishanahmed AR Shaikh
