---
title: "What Is Fault Managed Power?"
description: "Fault Managed Power (FMP) delivers safe electrical power over standard low-voltage wiring by monitoring and limiting fault energy in real time — no conduit, no service upgrade, no panel at the remote end."
summary: "FMP monitors every power packet 500 times per second and shuts off faults before they can cause shock or fire. The result: safe power delivery through standard structured cable, without conduit, without service upgrades."
slug: what-is-fmp
type: guides
weight: 10

knowledge_sources:
  - CLAIM_FMP_DEFINITION
  - CLAIM_DIGITAL_ELECTRICITY_MECHANISM
  - EXPL_FMP_ARCHITECTURE
  - MAP_AC_VS_FMP_FEATURES_COMPARISON
  - MAP_TRADITIONAL_ELECTRICAL_VS_DE_HEAT_PUMP_RETROFIT
  - CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS
  - CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY
  - CLAIM_FMP_COMPLIANCE_PATHWAY
  - RULESET_FMP_FIT_CONDITIONS
  - what_is_de.yaml
  - Digital_Edge_Belden.yaml
  - DC_800V_alternative.yaml
---

## The short version

Fault Managed Power (FMP) is a power delivery system that makes electricity safe in a different way than conventional wiring does.

Conventional power is made safe through insulation and overcurrent devices — breakers that trip in seconds after a fault develops. The underlying assumption is that the circuit will carry dangerous energy until something shuts it off.

FMP works the other way: the transmitter sends power as rapid, monitored pulses — 500 per second — and checks each pulse for fault conditions before the next one fires. If a fault is detected, the transmitter stops within a single pulse cycle (2 milliseconds). The fault energy never accumulates to a harmful level.

The practical consequence: power can be delivered safely through standard low-voltage structured cable — the same type used for data and communications wiring — without conduit, without junction boxes, and without a service upgrade at the building or room level.

FMP is also called **Digital Electricity (DE)**, the commercial name used by VoltServer, which introduced the first FMP products. The terms are used interchangeably throughout this site.

---

## How the system works

An FMP installation has three parts:

1. **Transmitter (headend)** — connects to an existing electrical panel; converts AC to high-voltage DC (nominally 336V); chops the DC into pulses; monitors every pulse for fault conditions; licensed electrician required for the panel connection
2. **FMP cable (managed power link)** — standard low-voltage cable (16 AWG pairs) routed through the building using Class 2 methods; no conduit required; can share trays and raceways with data cabling
3. **Receiver (load end)** — converts FMP output back to the AC or DC form required by the connected load; installed by a low-voltage technician in most jurisdictions

**What the transmitter actually monitors:** Touch faults, short circuits, ground faults, and arc faults. Each pulse is verified before the next is sent. A fault causes shutdown in under 2 milliseconds — faster than the human nervous system's pain response (approximately 10 milliseconds for a muscle contraction signal).

**Wire capacity:** Each 16 AWG pair carries approximately 1.5–2 kW at the receiver. A standard 4-inch conduit using 40% fill and 8 pairs delivers up to 144 kW — enough for a substantial fraction of a building's retrofit load in a single riser run.

---

## How it differs from conventional electrical distribution

| Attribute | Traditional AC | Fault Managed Power |
|---|---|---|
| Cable | 10–12 AWG copper in conduit | 16 AWG structured cable pairs, no conduit |
| Remote-end panel | Required | Not required |
| Pathway method | Conduit / raceway, permitted | Class 2 methods: cable trays, J-hooks, plenum |
| Commissioning | Standard electrical inspection | Transmitter validation run + AHJ review of safety model |
| Adding capacity | New branch circuit, new conduit | Run another cable in existing tray |
| Labor vs equipment balance | Labor-intensive field work | Equipment-intensive; less field labor |

The shift from labor to equipment is meaningful for retrofit projects: the hard cost in traditional wiring is field labor (conduit bending, panel work, permitting time). In FMP, the hard cost is the transmitter and receiver hardware. When pathways are constrained — older buildings, operational data centers, remote industrial sites — the trade is favorable.

---

## How it differs from PoE, Class 2, and standard DC framing

This is where most confusion arises. FMP is **not** a variant of PoE or Class 2 power-limited circuits. It is a distinct safety architecture.

| System | Max power | Max range | Code class |
|---|---|---|---|
| PoE (802.3bt, Type 4) | 71 W | 100 m | Class 2 / Article 725 |
| 48V DC (standard) | 80–90 W | 123–247 m | Varies |
| Fault Managed Power (FMP) | 1,500 W per receiver | 180 m at 1.5 kW; 2,000+ m at 170 W | Class 4 / Article 726 |

**PoE and Class 2** are made safe by limiting total power output. The circuit can't output enough energy to cause harm even in a fault condition. This works at tens of watts, but it caps out well below the kilowatts needed for HVAC, lighting circuits, or rack PDUs.

**FMP (Class 4)** delivers kilowatts — not watts — safely, not by limiting total power but by detecting and stopping faults before energy accumulates. The transmitter is the safety device. The cable is not the limiting factor.

The practical implication: FMP can replace branch-circuit wiring, not just extend PoE. A single transmitter can power heat pumps, lighting loads, rack equipment, or edge devices over runs that PoE cannot approach.

---

## Code recognition: NEC Class 4

FMP is recognized in the National Electrical Code as **Class 4** wiring — a separate category from Class 1, 2, and 3.

| NEC Edition | Article | Status |
|---|---|---|
| 2023 NEC | Article 726 | Current edition in most U.S. jurisdictions |
| 2026 NEC | Article 722 | Renumbered; same safety model |

Class 4 uses Class 2 installation methods (no conduit required, flexible routing) but allows Class 2-level installation at far higher power levels — because the transmitter, not passive current limiting, provides the safety.

For permitting: FMP installations require a licensed electrician for the transmitter panel connection and (in most jurisdictions) for the permit application. The AHJ documentation package includes UL listing numbers for the transmitter and receiver, the applicable NEC article, a safety model summary, and a one-line diagram.

> **A note on "first-time" permits:** Many jurisdictions have not yet permitted a Class 4 installation. Budget 2–4 additional weeks for AHJ education on the first project in a new jurisdiction. Repeat installs move significantly faster once the inspector has seen the transmitter's fault response demonstrated.

*[Knowledge gap: the knowledge files do not contain a complete AHJ documentation checklist in YAML format. See the [NEC Class 4 guide](/guides/nec-class-4-article-726/) for the current checklist. That guide should be treated as authoritative until a corresponding YAML block is created.]*

---

## Where FMP is most useful

FMP performs best when conventional wiring is pathway-constrained, schedule-constrained, or economically penalized by the need for a service upgrade.

**Strong fit conditions:**
- Long cable runs where traditional conduit would require significant labor or permitting
- Retrofits in occupied buildings where trenching or major disruption is not acceptable
- Distributed endpoints (many small loads across a large floor plate or building stack)
- Situations where a service or panel upgrade is the blocking constraint on the project
- Cases where "just enough" power per endpoint is needed at each location

**Weak fit conditions:**
- Short runs (under 100 ft) with easy conduit access — traditional wiring will likely be cheaper
- Greenfield construction where pathways are designed in from the start and labor costs are low
- A single very large load (250+ kW) at one point — FMP aggregates many drops, not one large one
- Sites where the headend panel connection is infeasible or prohibitively expensive

> **Synthesis:** FMP doesn't compete against all electrical distribution. It competes specifically against the cost and schedule of providing power where power is hard to get. The question to ask is not "is FMP cheaper than wire?" but "what is the total cost — including service upgrades, permitting delays, and disruption — of getting power to this location the conventional way?"

---

## The heat pump retrofit case

The clearest current application is multifamily building electrification — specifically, heat pump retrofits in older buildings.

The conventional path: a heat pump retrofit in a pre-1973 multifamily building typically requires a panel upgrade ($5,000–$15,000), feeder upgrades, and in many cases a service upgrade ($10,000–$30,000 per tier), with utility coordination timelines of 18–24 months. The combined effect: approximately 50% of heat pump retrofit projects in older buildings are canceled due to electrical upgrade costs alone.

The FMP path: the transmitter connects to the existing service at the electrical room. Cable runs through abandoned building risers — trash chutes, laundry chutes, mail chutes, steam risers — to receivers at each unit. No new penetrations in most cases. No service upgrade. Cost per drop: approximately $500–600. Timeline: weeks to months rather than years.

The target building profile for FMP heat pump retrofits: pre-1973 construction, 40A panels, failing or end-of-life hydronic heating systems, absorption chillers, medium-to-large building size.

---

## The data center case

In data centers, FMP addresses a different version of the same problem: too much power needed at too many points, with conventional distribution infrastructure that wasn't designed for current AI rack densities.

Average AI server rack density has reached approximately 27 kW (AFCOM 2025), well above the 8–15 kW assumption in most existing PDU and busway specifications. A conventional upgrade — new conduit, new panels, new busway — in an operational data center is slow and risky.

FMP cable runs in the same trays as data cabling. No intermediate distribution switchgear at the rack row. A 6 MW data center deployment using FMP runs approximately $13.4M installed (labor + material) versus $19.9M for conventional AC distribution — a 32.9% cost reduction, or $6.6M in absolute savings on one project.

---

## Who makes FMP systems

- **VoltServer** — Digital Electricity; first commercial FMP product; 1,000+ installations globally across data centers, edge, and building electrification
- **Cence Power** — Class 4 DC distribution for data centers and telecom
- **Belden** — manufactures FMPS cables (the first cables UL-listed specifically for Class 4)
- **Panduit** — Class 4 unshielded cable product line
- Additional OEMs entering as NEC adoption matures

---

## What to read next

- [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/) — permit and AHJ guidance
- [Where FMP Fits](/guides/where-fmp-fits/) — verticals and use case context
- [How FMP Is Installed](/guides/how-fmp-is-installed/) — installation steps and commissioning
- [Scoping and Estimating](/guides/scoping-and-estimating/) — cost drivers and pre-bid checklist
