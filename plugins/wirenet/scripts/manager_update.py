#!/usr/bin/env python3
"""Check the latest published wirenet Manager release without changing state."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from manager_model import PLUGIN_VERSION


LATEST_RELEASE_URL = "https://api.github.com/repos/wirenet-dev/wirenet/releases/latest"
UPDATE_COMMAND = "codex plugin marketplace upgrade wirenet"
POST_UPDATE_ACTION = "Start a fresh task and run $manager-setup."


def semantic_version(value: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z.-]+)?", value.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def concise_notes(body: str, *, limit: int = 3) -> list[str]:
    bullets: list[str] = []
    current: str | None = None
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and stripped[2:].strip():
            if current:
                bullets.append(current)
            current = stripped[2:].strip()
            continue
        if current and line[:1].isspace() and stripped:
            current = f"{current} {stripped}"
            continue
        if current:
            bullets.append(current)
            current = None
    if current:
        bullets.append(current)
    if bullets:
        return bullets[:limit]
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", body) if item.strip()]
    return paragraphs[:1]


def load_release(
    *,
    release_json: Path | None,
    timeout: float,
) -> dict[str, object]:
    if release_json is not None:
        payload = json.loads(release_json.read_text(encoding="utf-8"))
    else:
        request = Request(
            LATEST_RELEASE_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "wirenet-manager-update-check",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, OSError) as url_error:
            curl = shutil.which("curl")
            if not curl:
                raise url_error
            process = subprocess.run(
                [
                    curl,
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--location",
                    "--max-time",
                    str(timeout),
                    "--header",
                    "Accept: application/vnd.github+json",
                    "--header",
                    "User-Agent: wirenet-manager-update-check",
                    LATEST_RELEASE_URL,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if process.returncode != 0:
                detail = process.stderr.strip() or (
                    f"curl exited {process.returncode}"
                )
                raise RuntimeError(
                    f"GitHub release check failed: {detail}"
                ) from url_error
            payload = json.loads(process.stdout)
    if not isinstance(payload, dict):
        raise ValueError("release response must be a JSON object")
    return payload


def check_for_update(
    *,
    release_json: Path | None = None,
    timeout: float = 5.0,
) -> dict[str, object]:
    result: dict[str, object] = {
        "ok": True,
        "state": "current",
        "current_version": PLUGIN_VERSION,
        "latest_version": None,
        "update_available": False,
        "release_name": None,
        "release_notes": [],
        "release_url": None,
        "update_command": UPDATE_COMMAND,
        "post_update_action": POST_UPDATE_ACTION,
    }
    try:
        release = load_release(
            release_json=release_json,
            timeout=timeout,
        )
        tag = str(release.get("tag_name") or "").strip()
        latest = semantic_version(tag)
        current = semantic_version(PLUGIN_VERSION)
        if not tag or latest is None or current is None:
            raise ValueError("release or installed plugin version is not semantic")
        result.update(
            {
                "latest_version": tag.removeprefix("v"),
                "release_name": release.get("name") or tag,
                "release_notes": concise_notes(str(release.get("body") or "")),
                "release_url": release.get("html_url"),
                "update_available": latest > current,
                "state": "available" if latest > current else "current",
            }
        )
    except (
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
        HTTPError,
        URLError,
    ) as error:
        result.update(
            {
                "ok": False,
                "state": "unavailable",
                "error": str(error),
            }
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-json", type=Path)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()
    result = check_for_update(
        release_json=args.release_json,
        timeout=args.timeout,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
