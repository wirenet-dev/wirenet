#!/usr/bin/env python3
"""Install or remove the managed wirenet global block.

Writes a short, marker-delimited block into the runtime's global
instruction file so any session can route bound workspaces to the Manager.
Idempotent: an existing block is replaced in place. Dry-run-first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

START = "<!-- wirenet-manager:start -->"
END = "<!-- wirenet-manager:end -->"

BLOCK = f"""{START}
## wirenet Manager

The user's Manager lives at `~/Manager` — their durable work memory. Before
working in any project folder, check `~/Manager/.wirenet/workspace-bindings.json`;
if the folder is bound, read that pack's README first. After meaningful
progress in a bound workspace, propose a pack update (preview, then approval).
If a folder is unbound but looks durable, ask once whether to track it.
Never write secrets into the Manager.
{END}"""

TARGETS = {
    "claude": Path.home() / ".claude" / "CLAUDE.md",
    "codex": Path.home() / ".codex" / "AGENTS.md",
}


def apply(path: Path, remove: bool, dry_run: bool) -> dict:
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if START in text and END in text:
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        new = before.rstrip() + ("\n\n" + BLOCK if not remove else "") + after
        action = "removed" if remove else "replaced"
    elif remove:
        return {"file": str(path), "action": "absent"}
    else:
        new = (text.rstrip() + "\n\n" if text.strip() else "") + BLOCK + "\n"
        action = "added"
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
    return {"file": str(path), "action": action}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=[*TARGETS, "both"], default="both")
    parser.add_argument("--file", type=Path, help="explicit instruction file")
    parser.add_argument("--remove", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    files = [args.file.expanduser()] if args.file else [
        TARGETS[key] for key in (TARGETS if args.target == "both" else [args.target])
    ]
    results = [apply(path, args.remove, args.dry_run) for path in files]
    print(json.dumps({"ok": True, "dry_run": args.dry_run, "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
