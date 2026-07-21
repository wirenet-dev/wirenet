---
last_edited: 2026-07-21
---

# Managed WireNet Installations

WireNet can be installed for one person or operated for an organization without
turning customer state into product state. The product repository distributes
behavior; each installation owns its data and its repositories.

## Ownership Boundary

- A Manager belongs to one person. Shared work is linked or promoted into an
  organization Base instead of making one Manager canonical for a team.
- A Base belongs to one organization and holds its shared knowledge, system
  descriptions, decisions, and data catalog.
- A Shelf belongs to one organization and holds executable or installable
  capabilities that organization is allowed to use.
- Client Runtime files stay with the project, repository, or operational system
  whose work they govern.
- The public product repository contains templates, schemas, migrations, and
  reusable plugins only.

## Repository And Access Model

The client or owning organization creates and owns the private Base and Shelf
repositories. Authorized people and service operators receive normal,
revocable collaborator access. Local clones may exist on multiple devices, but
Git history and the organization's review policy determine the shared state.
WireNet does not create remotes or accounts during local initialization.

Personal and customer repositories should use explicit namespaces and access
policies. Secrets, credentials, raw customer exports, and private source dumps
must not be copied into the product repository or a cross-customer index.

## Installation And Updates

`wirenet init base|shelf` is dry-run-first. With `--apply`, it materializes a
versioned product seed, writes an instance-origin manifest, and registers the
local path in `~/.wirenet/installation.json`. It does not initialize or connect
a Git remote.

Updates are opt-in and one way:

1. WireNet publishes a product version with templates or a migration.
2. The installation previews the applicable change.
3. The owner approves and applies it inside the instance repository.
4. The instance keeps its own review and Git history.

Instance knowledge and proprietary skills never become an upstream product
input automatically. A capability can enter the public product only through a
separate, intentional contribution with verified provenance and licensing.

## Managed Service Boundary

"Managed" describes an operating role, not a new storage tier. The operator
may maintain client-owned Base and Shelf repositories, run health checks, and
propose upgrades under the client's approval and access rules. The client's
repositories remain canonical.

A hosted control plane is deliberately deferred. It becomes justified only
when real operations require cross-installation inventory, policy enforcement,
remote health, billing, or coordinated rollout. Until then, repository access,
the local installation manifest, and explicit runbooks are the smaller and more
auditable system.
