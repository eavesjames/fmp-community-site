---
title: "The Three-Way Lock: Why GPU Rack Deployments Break Sequential MEP Design Workflows"
date: 2026-03-06
draft: true
insight_id: "2026-03-06-A02"
status: "DRAFT"
levers: []
which_verticals: []
confidence: ""
must_cite_items: ["98", "52", "76", "100"]
---

## Thesis

AI/GPU rack deployments at 40+ kW per rack force simultaneous redesign of electrical distribution, liquid cooling, and UPS architecture—three systems with circular design dependencies that standard sequential MEP workflows cannot resolve. Cooling infrastructure placement must be locked before electrical conduit routing is finalized; electrical routing must be locked before PDU specification is confirmed; UPS battery sizing cannot be confirmed until actual GPU power draw is verified post-IT-procurement. This circular dependency creates systematic mid-project design conflicts and change-order risk that is independent of the technical solutions chosen for each system. Facilities that adopt integrated concurrent design workflows and pre-stage flexible infrastructure (3-phase feeders to anticipated GPU zones, modular PDU configurations, scalable UPS topology) can reduce change-order exposure by 30–50% on GPU deployment projects.

## Why this is new

_Explain why this angle is original._

## Who cares

_Specify target audience._

## Recommended questions to research

- On your most recent GPU rack deployment project, which constraint hit first in the field—cooling hardware blocking conduit access, PDU spec mismatch requiring reorder, or UPS battery sizing change due to confirmed power draw differing from IT estimate? How many weeks of schedule delay resulted?
- Do you currently use a shared power-density model that all three trades (cooling, electrical, UPS) update simultaneously during design, or does each trade receive a separate scope document? If separate, at what project milestone do you reconcile conflicts?
- What is your current standard for pre-staging electrical infrastructure to future GPU-dense zones—do you install 3-phase feeders speculatively, or only after IT procurement confirms GPU equipment?

## Evidence gaps to fill

- Project post-mortem data from at least two GPU rack deployments showing root-cause analysis of schedule delays attributable to cooling-electrical-UPS sequencing conflicts vs. other causes.
- Electrical feeder sizing rules and cost estimates ($/linear foot, conduit fill, voltage drop) for 3-phase 60A and 100A feeds to 40 kW rack zones in retrofitted facilities.
- Rear-door liquid cooler physical dimensions and installation clearance requirements relative to PDU placement and conduit routing constraints in standard 48U racks.
- Lead time and cost premium for BTO/ETO PDUs at 60A and 100A three-phase configurations from Raritan, Vertiv, and Schneider to quantify the procurement risk from late PDU specification.

## Must-cite items

- item 98: Liquid Cooling for High-Density Data Center Racks: Power and Thermal Constraints
- item 52: Rack Density Keeps Rising at Enterprise Data Centers
- item 76: Guide to Intelligent Rack Power Distribution for Data Centers
- item 100: UPS Runtime Reduction: Battery Technology Trade-offs for Data Centers
