---
title: "Where FMP Fits: Verticals, Use Cases, and Fit Conditions"
description: "FMP is not a universal replacement for conventional electrical distribution. It is strongest in constrained retrofits, long distributed runs, and projects where the conventional path is blocked by cost or schedule. Here's how to identify good candidates quickly."
summary: "FMP wins when the conventional wiring path is expensive, constrained, or blocked by a service upgrade. It does not win on commodity wiring cost. Here's the fit framework, the quick qualification checklist, and the three verticals where it creates the most value."
slug: where-fmp-fits
type: guides
weight: 30

knowledge_sources:
  - RULESET_FMP_FIT_CONDITIONS
  - CHK_FMP_FIELD_QUALIFICATION
  - MAP_TECH_TO_OWNER_VALUE
  - CLAIM_FMP_LABOR_SHIFT
  - CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS
  - CLAIM_IDEAL_BUILDING_CHARACTERISTICS_HEAT_PUMP_RETROFIT
  - MAP_TRADITIONAL_ELECTRICAL_VS_DE_HEAT_PUMP_RETROFIT
  - CLAIM_CLASS4_VS_CLASS2_CLASS3
---

## Introduction

The right question to ask about any FMP project is not "is FMP cheaper than wire?" It is: *what is the total cost — material, labor, permits, service upgrades, schedule delay, and occupant disruption — of getting power to this location the conventional way?*

FMP does not win on commodity wiring cost. It wins when the total conventional path is expensive, slow, or infeasible. That distinction matters for qualification: a short run in a new building with easy conduit access and cheap labor is not a good FMP candidate. A 20-floor retrofit in an occupied building with no available risers and an 18-month service upgrade queue is exactly what FMP is designed for.

---

## The fit framework

FMP is a strong candidate when conventional AC distribution would be pathway-labor intensive, schedule-disruptive, or constrained by retrofit conditions.

**Strong fit conditions:**
- Long cable runs where conduit and branch-circuit buildout become expensive and slow
- Retrofits in occupied buildings where pathway access is constrained and disruption costs are high
- Projects with high schedule value — downtime costs, tenant disruption penalties, or regulatory deadlines
- Distributed endpoints — many loads across a large floor plate or building stack — where repeatable, standardized drops reduce per-unit cost
- Projects where the conventional path requires a panel or service upgrade that is cost-prohibitive or timeline-blocking

**Weak fit conditions:**
- Short, simple runs with easy conduit access and low field labor cost
- Greenfield construction with abundant pathway space designed in from the start
- A single very large load at one location — FMP aggregates many distributed drops; it does not compete with a single large AC feeder
- Sites where the transmitter headend location is infeasible — no panel access, no rack space, no suitable electrical room

*The decision logic: if AC pathway work is difficult or expensive, FMP moves to the top of the list. If run lengths are long and endpoints are many, the FMP advantage grows. If the run is short, simple, and labor is cheap, AC will likely win.*

---

## Quick qualification checklist

Use these six questions to qualify a project before investing in detailed estimating. If three or more answers are yes, treat it as an FMP candidate and run a ROM estimate.

1. Is this a retrofit with pathway or riser constraints?
2. Are run lengths long, or is routing complex — firestopping, asbestos, structural issues?
3. Is speed to market valuable — does downtime or tenant disruption have a real cost?
4. Are there many endpoints where repeatable drops would help?
5. Would AC require panel upgrades, new risers, or heavy conduit work?
6. *(If no to most of the above)* Is this a short, simple run with cheap labor — does AC likely win?

Three or more yes answers to questions 1–5 puts the project in the FMP column. A strong yes to question 6 takes it back out.

---

## What owners are actually buying

Owners do not buy wiring theory. They buy schedule, disruption reduction, and risk reduction. Understanding this translation is the difference between a technical pitch and a sale.

| What FMP does technically | What the owner actually gets |
|---|---|
| Reduced pathway and conduit work | Less disruption, fewer trades on site, faster schedule, less patch-and-restore |
| Repeatable drops to endpoints | Predictable unit cost; scalable rollout without re-engineering |
| Avoids major electrical upgrades | Lower capex and fewer occupant impacts for retrofits |

The contractor's job is to translate from column one to column two. "We don't need conduit" is a technical fact. "You can keep units occupied during the installation" is what the owner hears.

---

## Multifamily building retrofits

**The problem:** Older multifamily buildings — pre-1973 construction, 40-amp panels, failing hydronic heating systems — don't have the electrical capacity for heat pump retrofits. The conventional path costs approximately $20,000 per unit, takes up to two years including utility coordination, and forces occupants out of their units during major electrical work. Roughly 50% of heat pump retrofit projects in these buildings are canceled because of this barrier alone.

**The target building profile:** Pre-1973 construction. 40A panels. Failing or aging hydronic heating or absorption chiller systems. Building envelope with no clear pathway for new conduit — or with available abandoned risers (steam, trash, laundry, or mail chutes) that FMP can use instead.

**How FMP changes the equation:**
- A transmitter rack connects to the existing electrical service at the electrical room — no service upgrade required
- Structured cable runs through abandoned risers — no new penetrations in most buildings
- Receivers at each unit deliver 240V AC to the heat pump
- Cost per unit drops from ~$20,000 for the conventional path to a fraction of that per drop

For buildings facing Local Law 97 penalties or similar building performance standards, where traditional upgrade timelines run 18–24 months and the compliance deadline is fixed, FMP may be the only viable path for projects starting in 2025 or 2026.

---

## Data centers

**The problem:** AI workloads have pushed average rack density well above what most existing PDU and busway infrastructure was designed for. Standard distribution can't accommodate current densities without major civil work — raised floor reconfiguration, new busway infrastructure, added switchgear.

**How FMP fits:**
- New power distribution pathways share cable trays with low-voltage data cabling — no conduit rerouting or raised-floor reconfiguration
- Distributed endpoint model suits high-density AI cluster rows and edge-of-row power delivery
- Class 4 wiring can share pathways with data cable, reducing the civil work required to add new circuits
- In a 6 MW data center reference scenario, FMP distribution runs approximately $13.4 million installed versus $19.9 million for equivalent conventional AC distribution — a savings of roughly $6.6 million, or 32.9%

The data center application is structurally similar to the multifamily retrofit: too much power needed at too many points, with existing infrastructure that wasn't built for current densities.

---

## Edge and distributed infrastructure

**The problem:** Edge sites — telecom aggregation points, building IoT infrastructure, streetside or campus deployments — need reliable power at remote locations, often in spaces that were never designed for traditional electrical runs. The conventional path requires dedicated conduit to each endpoint, individual branch circuits, and often additional switchgear.

**How FMP fits:**
- Delivers power over standard low-voltage cable to remote endpoints without dedicated conduit
- A single transmitter can serve multiple endpoints across a building or campus
- Relevant for applications needing more than PoE (802.3bt tops out at ~90 W) but where running conventional AC branch circuits to each point is impractical
- Commissioning and diagnostics are centralized at the transmitter rather than distributed at each endpoint

---

## The labor-to-equipment cost shift

On projects where FMP fits, it typically shifts cost from field labor — conduit bending, pathway work, panel scheduling, heavy cable pulling — to equipment: transmitters and receivers. That shift has two effects beyond the headline cost number:

1. **Schedule**: equipment cost is predictable and front-loaded; field labor cost is subject to change orders, site conditions, and trade availability. Converting labor to equipment improves schedule predictability.
2. **Scalability**: adding endpoints to an FMP system is adding another cable run and receiver, not opening another panel schedule and pulling conduit to a new subpanel. This matters for phased rollouts and buildings where the load profile is expected to change.

The labor-to-equipment shift is not universal — on short, simple runs with cheap labor, the equipment cost of transmitters and receivers will dominate and FMP will lose on price. The shift is the story on constrained retrofits and long distributed runs.

---

## Related guides

- [What Is Fault Managed Power?](/guides/what-is-fmp/) — how the system works
- [Scoping and Estimating an FMP Project](/guides/scoping-and-estimating/) — ROM workflow and cost drivers
- [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/) — code and compliance framing
