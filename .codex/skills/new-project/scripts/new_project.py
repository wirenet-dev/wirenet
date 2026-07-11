from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SHARED_SCRIPTS = Path(__file__).resolve().parents[2] / "onboarding" / "scripts"
sys.path.insert(0, str(SHARED_SCRIPTS))

from vault_model import (  # noqa: E402
    ensure_project_router,
    insert_router_entry,
    render_project_agents,
    render_project_readme,
)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-project"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a project or experiment.")
    parser.add_argument("name")
    parser.add_argument("--type", choices=["project", "experiment"], default="project")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--slug", default="")
    parser.add_argument("--no-agents", action="store_true")
    parser.add_argument(
        "--vault-dir",
        default=str(ROOT),
        help="Vault root path. Defaults to the repository containing this script.",
    )
    args = parser.parse_args()

    vault_dir = Path(args.vault_dir).expanduser().resolve(strict=False)
    stamp = date.today().isoformat()
    entry_id = args.slug or slugify(args.name)
    if args.type == "experiment":
        if not entry_id.startswith("exp-"):
            entry_id = f"exp-{entry_id}-{stamp}"
        root_dir = vault_dir / "experiments"
        template = vault_dir / "templates" / "experiment_README.md"
        readme = template.read_text(encoding="utf-8").replace("<Experiment Name>", args.name)
        readme = readme.replace("<Summary>", args.summary)
        agents = (vault_dir / "templates" / "PROJECT_AGENTS.md").read_text(encoding="utf-8")
        router_update: tuple[Path, str] | None = None
    else:
        root_dir = vault_dir / "projects"
        project_dir = root_dir / entry_id
        if project_dir.exists():
            raise FileExistsError(f"path already exists: {project_dir.relative_to(vault_dir).as_posix()}")
        router_path, router = ensure_project_router(vault_dir, dry_run=True)
        try:
            router_update = (router_path, insert_router_entry(router, entry_id, args.name))
        except ValueError as error:
            raise SystemExit(str(error)) from error
        readme = render_project_readme(args.name, args.summary)
        agents = render_project_agents(args.name)

    project_dir = root_dir / entry_id
    rel_path = project_dir.relative_to(vault_dir).as_posix()
    if project_dir.exists():
        raise FileExistsError(f"path already exists: {rel_path}")

    project_dir.mkdir(parents=True)
    (project_dir / "README.md").write_text(readme, encoding="utf-8")
    if not args.no_agents:
        (project_dir / "AGENTS.md").write_text(agents, encoding="utf-8")
    if router_update:
        router_update[0].parent.mkdir(parents=True, exist_ok=True)
        router_update[0].write_text(router_update[1], encoding="utf-8")

    print(f"created: {rel_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
