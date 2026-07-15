#!/usr/bin/env python3
"""Compare WireNet Manager with its Jason Liu upstream without merging changes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        capture_output=True,
        text=True,
    )


def lines(result: subprocess.CompletedProcess[str]) -> list[str]:
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--upstream", default="upstream/main")
    parser.add_argument("--fetch", action="store_true", help="Fetch and prune the upstream remote first.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve(strict=False)
    if args.fetch:
        remote = args.upstream.split("/", 1)[0]
        fetched = run(repo, "fetch", "--prune", remote, check=False)
        if fetched.returncode != 0:
            result = {
                "ok": False,
                "repo": str(repo),
                "upstream": args.upstream,
                "error": fetched.stderr.strip() or "upstream fetch failed",
            }
            print(json.dumps(result, indent=2) if args.json else result["error"])
            return 1

    verify = run(repo, "rev-parse", "--verify", args.upstream, check=False)
    if verify.returncode != 0:
        result = {
            "ok": False,
            "repo": str(repo),
            "upstream": args.upstream,
            "error": f"unknown upstream ref: {args.upstream}",
        }
        print(json.dumps(result, indent=2) if args.json else result["error"])
        return 2

    head = run(repo, "rev-parse", "HEAD").stdout.strip()
    upstream = verify.stdout.strip()
    merge_base = run(repo, "merge-base", "HEAD", args.upstream).stdout.strip()
    ahead_raw, behind_raw = run(
        repo,
        "rev-list",
        "--left-right",
        "--count",
        f"HEAD...{args.upstream}",
    ).stdout.split()
    result = {
        "ok": True,
        "repo": str(repo),
        "head": head,
        "upstream_ref": args.upstream,
        "upstream_commit": upstream,
        "merge_base": merge_base,
        "ahead": int(ahead_raw),
        "behind": int(behind_raw),
        "upstream_commits": lines(
            run(repo, "log", "--format=%h %s", f"HEAD..{args.upstream}")
        ),
        "wirenet_commits": lines(
            run(repo, "log", "--format=%h %s", f"{args.upstream}..HEAD")
        ),
        "committed_delta": lines(
            run(repo, "diff", "--name-status", f"{merge_base}..HEAD")
        ),
        "worktree_delta": lines(run(repo, "status", "--short")),
    }

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"WireNet Manager: {result['ahead']} ahead, {result['behind']} behind {args.upstream}")
    for heading, key in (
        ("New upstream commits", "upstream_commits"),
        ("WireNet commits", "wirenet_commits"),
        ("Committed file delta", "committed_delta"),
        ("Working tree delta", "worktree_delta"),
    ):
        print(f"\n{heading}:")
        entries = result[key]
        if entries:
            for entry in entries:
                print(f"- {entry}")
        else:
            print("- none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
