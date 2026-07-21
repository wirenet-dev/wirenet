# Manager/Base Through Meadows' Lens

## 1. Stocks, Flows, Feedback Loops

**Stocks**
- *Personal knowledge stock*: the packet corpus in `~/Manager` (projects/, people/, experiments/, agent/) — accumulated durable context.
- *Org knowledge stock*: Base — certified, shared packets.
- *Trust stock* (implicit, critical): the reader-agent's confidence that what a packet says is still true. This stock, not the file count, is what the product actually sells.

**Inflows**
- Packet writes at task end, regulated by the update threshold ("only when a future task would otherwise misunderstand") — a valve on inflow that keeps the stock compact.
- The preview-and-approve gate — a second, human-held valve in series on the same inflow.
- For Base: git merges by owners — certification is an inflow valve with a named valve-keeper.

**Outflows**
- *Memory rot*: reality diverges from packets with no corresponding write. This outflow is continuous, silent, and — as designed — largely unregulated. Nothing drains a stale claim out of the stock; it just becomes wrong in place.
- Explicit archiving (`archive/`) is the only deliberate outflow, and it is manual.

**Feedback loops**
- *Balancing*: doctor/staleness checks compare `last_edited` against a review cadence and flag drift — a thermostat on the trust stock. Review cadences set the loop's sampling rate.
- *Balancing*: the update threshold damps inflow oscillation (no packet churn from routine edits).
- *Reinforcing (virtuous)*: agents that read good packets produce better work, which produces better packet updates. This is the engine of the product.
- *Reinforcing (vicious)*: agents that hit one stale packet trust the stock less, read it less, update it less — trust collapse is self-accelerating.

## 2. Meadows' Leverage Points

**Already used**
- *#12 Parameters / #10 Stock-flow structure*: review cadence intervals, folder taxonomy, frontmatter schema.
- *#11 Buffers*: `outputs/` and `sources/` as non-canonical buffers that keep noise out of the canonical stock.
- *#6 Information flows*: the strongest existing lever — doctor checks surface staleness to the actor who can fix it; git history makes every stock change inspectable; Base merges make certification visible.
- *#5 Rules*: the update threshold, "no raw media/secrets in canonical knowledge," owner-only merges. These rules are the design's real backbone.

**Missed or weak**
- *#8 Strength of balancing loops relative to the drift they fight*: rot rate scales with work velocity; doctor cadence is fixed. Under load the balancing loop loses.
- *#6, other direction*: no feedback from **read-time failure** — when an agent finds a packet wrong mid-task, nothing routes that signal into the stock. The most valuable error signal is discarded.
- *#4 Self-organization*: schema v0.2 evolves only by hand; the system can't grow new packet types from observed need.
- *#3 Goals*: the operative goal can silently become "keep packets tidy" instead of "keep future tasks from misunderstanding." No metric measures the latter.
- *#2 Paradigm*: git-merge certification imports code's paradigm — that certified-at-merge-time means correct-now. Knowledge decays after merge; code mostly doesn't.

## 3. Design Rules (adopt these)

1. Every read is a doctor check: when an agent uses a packet and observes it contradicted by reality, it must file the discrepancy in that same turn — closing the missing rot-detection loop at the point of highest signal.
2. Scale review cadence to write velocity, not calendar time: a packet touched weekly gets checked weekly; a dormant one gets a longer clock plus an explicit "dormant, may be stale" banner — matching the balancing loop's gain to the outflow it fights.
3. Certification in Base must carry an expiry, not just an owner: a merge asserts "true as of date X, recheck by date Y," turning certification from a one-time event into a renewable stock.
4. Measure the goal, not the proxy: track "packet consulted and contradicted" incidents per week as the product's north-star error rate, so the system's goal stays "future tasks understand correctly," not "files look maintained."
5. Make deletion as cheap as addition: give the doctor authority to propose archiving, because a stock with regulated inflow and no outflow monotonically accumulates rot.

## 4. Traps to Name

- **Drift to low performance**: each stale packet that goes unpunished lowers the perceived standard ("packets are usually roughly right"); agents then write to that standard, and the trust stock erodes ratchet-wise. Antidote: absolute standard — the contradicted-packet metric — not comparison to last month's stock.
- **Shifting the burden**: capable agents route around a wrong packet by re-deriving context from git log, email, and source files. The task succeeds, the symptom disappears, the packet stays wrong — and the organization becomes dependent on heroic per-task re-derivation instead of fixing the stock. The update threshold makes this worse: a quiet workaround never crosses "a future task would misunderstand" in the acting agent's judgment.
- **Rule beating**: agents satisfying the update threshold's letter with trivial `last_edited` bumps that reset the doctor's staleness clock without renewing content — the balancing loop reads "fresh," the stock is not.
- **Seeking the wrong goal (Base)**: if merge count or certification coverage becomes the KPI, owners certify liberally and Base becomes a large, credentialed, wrong stock — worse than a small honest one, because certification actively suppresses reader skepticism.