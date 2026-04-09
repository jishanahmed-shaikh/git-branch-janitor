"""CLI entry point for git-branch-janitor."""

import sys
import argparse
from janitor.core import get_merged_branches, delete_branch
from janitor import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-janitor",
        description="Delete local git branches already merged into main.",
    )
    parser.add_argument(
        "--base",
        default="main",
        help="Base branch to check merges against (default: main)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show branches that would be deleted without actually deleting them",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt and delete immediately",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"git-janitor {__version__}",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        branches = get_merged_branches(base=args.base)
    except RuntimeError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    if not branches:
        print(f"✅ No merged branches to clean up against '{args.base}'. All tidy.")
        return

    print(f"\n🌿 Merged branches (base: {args.base}):\n")
    for b in branches:
        print(f"   {b}")

    if args.dry_run:
        print(f"\n[dry-run] {len(branches)} branch(es) would be deleted. No changes made.\n")
        return

    if not args.yes:
        answer = input(f"\nDelete {len(branches)} branch(es)? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            return

    print()
    deleted, failed = 0, 0
    for branch in branches:
        ok, msg = delete_branch(branch)
        if ok:
            print(f"  🗑️  {msg}")
            deleted += 1
        else:
            print(f"  ❌ Failed to delete '{branch}': {msg}")
            failed += 1

    print(f"\n  Done. {deleted} deleted, {failed} failed.\n")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
