#!/usr/bin/env python3
"""Refresh the Manager's qmd collection — explicit maintenance only.

Never runs a global `qmd update`; touches only the named collection. If qmd
is not installed, reports that and exits cleanly (qmd is optional).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", default="manager")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if shutil.which("qmd") is None:
        print(json.dumps({"ok": True, "qmd": "not installed", "note": "qmd is optional; the Manager works without it"}))
        return 0
    command = ["qmd", "update", args.collection]
    if args.dry_run:
        print(json.dumps({"ok": True, "dry_run": True, "would_run": command}))
        return 0
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print(json.dumps({
        "ok": result.returncode == 0,
        "command": command,
        "stdout": result.stdout.strip()[-2000:],
        "stderr": result.stderr.strip()[-2000:],
    }, indent=2))
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
