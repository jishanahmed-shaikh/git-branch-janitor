"""Tests for janitor.core using mocked subprocess calls."""

import pytest
from unittest.mock import patch, MagicMock
from janitor.core import (
    get_current_branch,
    get_merged_branches,
    delete_branch,
    PROTECTED,
)


def make_run(returncode=0, stdout="", stderr=""):
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    m.stderr = stderr
    return m


@patch("janitor.core.subprocess.run")
def test_get_current_branch(mock_run):
    mock_run.return_value = make_run(stdout="feature/my-branch\n")
    assert get_current_branch() == "feature/my-branch"


@patch("janitor.core.subprocess.run")
def test_get_merged_branches_filters_protected(mock_run):
    mock_run.side_effect = [
        make_run(stdout="  main\n  feature/done\n  develop\n  old-fix\n"),
        make_run(stdout="feature/active\n"),  # current branch
    ]
    branches = get_merged_branches(base="main")
    assert "main" not in branches
    assert "develop" not in branches
    assert "feature/done" in branches
    assert "old-fix" in branches


@patch("janitor.core.subprocess.run")
def test_get_merged_branches_excludes_current(mock_run):
    mock_run.side_effect = [
        make_run(stdout="  feature/wip\n  feature/done\n"),
        make_run(stdout="feature/wip\n"),  # current branch
    ]
    branches = get_merged_branches(base="main")
    assert "feature/wip" not in branches
    assert "feature/done" in branches


@patch("janitor.core.subprocess.run")
def test_get_merged_branches_raises_on_error(mock_run):
    mock_run.return_value = make_run(returncode=1, stderr="not a git repo")
    with pytest.raises(RuntimeError, match="git branch --merged failed"):
        get_merged_branches()


@patch("janitor.core.subprocess.run")
def test_delete_branch_success(mock_run):
    mock_run.return_value = make_run(stdout="Deleted branch old-fix")
    ok, msg = delete_branch("old-fix")
    assert ok is True
    assert "old-fix" in msg or "Deleted" in msg


@patch("janitor.core.subprocess.run")
def test_delete_branch_failure(mock_run):
    mock_run.return_value = make_run(returncode=1, stderr="branch not found")
    ok, msg = delete_branch("ghost-branch")
    assert ok is False
    assert "branch not found" in msg


def test_protected_set_contains_defaults():
    for b in ("main", "master", "develop", "staging"):
        assert b in PROTECTED
