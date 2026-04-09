"""Core logic for detecting and deleting merged git branches."""

import subprocess
from typing import List, Tuple


PROTECTED = {"main", "master", "develop", "dev", "staging", "production"}


def run(cmd: List[str], cwd: str = ".") -> Tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_current_branch(cwd: str = ".") -> str:
    """Return the name of the currently checked-out branch."""
    _, out, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd)
    return out


def get_merged_branches(base: str = "main", cwd: str = ".") -> List[str]:
    """
    Return local branches fully merged into `base`, excluding protected ones
    and the currently active branch.
    """
    code, out, err = run(["git", "branch", "--merged", base], cwd)
    if code != 0:
        raise RuntimeError(f"git branch --merged failed: {err}")

    current = get_current_branch(cwd)
    branches = []
    for line in out.splitlines():
        name = line.strip().lstrip("* ").strip()
        if name and name not in PROTECTED and name != current:
            branches.append(name)
    return branches


def delete_branch(branch: str, cwd: str = ".") -> Tuple[bool, str]:
    """
    Delete a local branch. Returns (success, message).
    Uses -d (safe delete — only merged branches).
    """
    code, out, err = run(["git", "branch", "-d", branch], cwd)
    if code == 0:
        return True, out or f"Deleted branch '{branch}'"
    return False, err
