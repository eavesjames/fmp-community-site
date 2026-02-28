---
title: "NEC Class 4 / Article 726: What Electricians and AHJs Need to Know"
description: "NEC Class 4 (Article 726 in the 2023 NEC; Article 722 in the 2026 NEC) is the code pathway for fault managed power systems. It is separate from Class 2 and Class 3 — different safety model, different wiring rules, same installation methods."
summary: "Class 4 is a distinct NEC wiring category, not a variant of Class 2. The safety model is different, the article number is different, and the power ceiling is different. Here's what installers and inspectors need to know about permits, article numbers, and the 2026 NEC transition."
slug: nec-class-4-article-726
type: guides
weight: 20

knowledge_sources:
  - CLAIM_CLASS4_VS_CLASS2_CLASS3
  - CLAIM_FMP_DEFINITION
  - CLAIM_NEC_ARTICLE_722_TRANSITION
  - PROC_AHJ_DOCUMENTATION_CHECKLIST
  - CLAIM_FMP_COMPLIANCE_PATHWAY
  - OBJ_COMMON_CONTRACTOR
---

## Introduction

The most common early mistake on an FMP installation is citing the wrong NEC article. Installers familiar with low-voltage and data work see Class 4 cable running through the same pathways as structured data cable and assume it falls under Article 725 — the Class 2 and Class 3 article. It does not.

Class 4 is a distinct circuit category with its own article, its own safety model, and its own listing requirements. Getting the article number right on a permit submission isn't a technicality — it's what lets the AHJ evaluate the installation correctly and issue the permit without a hold.

---

## Two article numbers, one safety model

The 2026 NEC renumbered Class 4 from Article 726 to Article 722. The safety model, installation requirements, and listing basis are unchanged — only the article number changed.

| NEC Edition | Article | Status |
|---|---|---|
| 2020 NEC | 726 | Class 4 introduced |
| 2023 NEC | 726 | Current edition in most U.S. jurisdictions |
| 2026 NEC | 722 | Renumbered; same safety model |

**During the transition period**, permit packages should cite both article numbers with their edition years: *"Article 726 (2023 NEC) / Article 722 (2026 NEC)."* An AHJ on the 2023 edition may not recognize Article 722 in newer product documentation. An AHJ on the 2026 NEC may not recognize Article 726 in older manufacturer submittals. Citing both prevents holds from either direction.

The most common mistakes during the transition:
- Citing only Article 726 to an AHJ on the 2026 NEC
- Citing only Article 722 to an AHJ on the 2023 or 2020 NEC
- Failing to confirm which NEC edition the jurisdiction has adopted before submitting

---

## How Class 4 differs from Class 2 and Class 3

This distinction matters for every FMP permit. Class 2 and Class 3 circuits (Article 725) are safe because they are power-limited — the output is capped too low to sustain a hazardous fault. Class 4 circuits are safe because they are fault-managed — the output is not power-limited, but a transmitter monitors every power delivery cycle and interrupts faults before hazardous energy accumulates.

| Attribute | Class 2 | Class 3 | Class 4 (FMP) |
|---|---|---|---|
| NEC Article | 725 | 725 | 726 (2023) / 722 (2026) |
| Safety mechanism | Power-limited: output capped below harmful threshold | Power-limited: output capped below harmful threshold | Fault-managed: transmitter monitors and stops faults in under 2 ms |
| Max power | 100 VA | 100 VA | Multiple kW per cable run; limited by transmitter model |
| Conduit required | No | No | No (follows Class 2 installation methods) |
| Can share raceway with data cable | Yes | Yes | Yes (Class 4 may share with Class 2 / low-voltage data) |
| Licensed electrician at load end | Generally not required | Generally not required | Verify local amendments; often not required at load end |

The practical upshot: Class 4 can deliver kilowatts through the same physical cable and installation methods that Class 2 uses for watts. The cable doesn't know the difference. The transmitter is what makes the system safe — and what requires the listing.

---

## What Class 4 allows

Because Class 4 follows Class 2 installation methods, an FMP installation can:

- Route cable without conduit — J-hooks, cable trays, plenum spaces, existing pathways
- Share cable trays and raceways with low-voltage data cabling
- Run through abandoned building risers — steam, trash, laundry, mail chutes
- Terminate at the load end without a licensed electrician in most jurisdictions (verify local amendments)
- Use standard 16 AWG structured cable pairs

What Class 4 cannot do:
- Mix in the same conduit as line-voltage wiring
- Operate without a listed transmitter — the transmitter listing is what authorizes the installation

The transmitter is the listed safety device. The cable is not the limiting factor, and there is no subpanel or branch circuit protection required at the remote end.

---

## The compliance pathway: listings anchor the permit

FMP compliance rests on two things: a product listing and the correct NEC article citation. The listing establishes that the transmitter and receiver meet the safety standard (UL 1400-1 for transmitters; UL 1400-2 for receivers). The NEC article establishes the installation requirements.

Contractors must anchor every compliance claim to specific listing numbers and a specific code reference. Vague references to "Class 4" or "low-voltage" without UL listing numbers and a NEC article citation are the most common cause of permit holds in jurisdictions unfamiliar with FMP.

*The compliance claim has two parts: what the product is listed to, and which code article governs the installation. Both must be in the permit package.*

---

## AHJ documentation package for a first-time submission

A complete package for the first Class 4 permit in a new jurisdiction includes five elements:

1. **UL listing number(s) for the transmitter** — e.g., UL 1400-1. Establishes the product listing basis for the installation.
2. **UL listing number(s) for the receiver(s)** — e.g., UL 1400-2. The receiver listing is separate from the transmitter.
3. **NEC article citation — cite both editions** — Article 726 (2023 NEC) / Article 722 (2026 NEC), with edition years.
4. **Safety model summary** — how fault detection works, the maximum fault energy, and the fault response time (under 2 ms). Many AHJs are unfamiliar with Class 4; the safety model summary is what justifies the wiring method to an inspector who has only ever seen Class 2.
5. **One-line diagram** — panel → transmitter → cable → receiver → load. Standard permit requirement that shows the scope and connection points.

Recommended addition: contact information for an AHJ technical resource — the FMP Alliance ([fmpalliance.com](https://fmpalliance.com)) or NFPA — for inspector questions. First-time inspectors frequently want a third-party technical resource available before issuing a permit.

---

## First-time jurisdiction: what to expect

On the first Class 4 installation in a jurisdiction that has not previously permitted one, budget 2–4 weeks of additional time for AHJ education before permit issuance. This is normal and not a sign of a problem.

Inspectors will typically want to:
- Review the safety model summary in detail
- Verify UL listing numbers independently
- See the transmitter's fault response demonstrated — bring the OEM datasheet showing max fault energy and response time, and be prepared for a simulated fault test during inspection

Repeat installations in the same jurisdiction move significantly faster once the AHJ is familiar with the system. The investment in the first permit package pays forward.

---

## Common errors that cause permit holds

- **Wrong article number** — citing Article 725 (Class 2/3) instead of Article 726/722 (Class 4)
- **Missing UL listing numbers** — submitting without the transmitter and receiver listing numbers; these are required, not optional
- **No safety model summary** — submitting a one-line diagram without explaining how the fault management works; this is the most common cause of inspector questions in unfamiliar jurisdictions
- **Single-edition NEC citation during transition** — citing only the 2023 or only the 2026 article number without noting the other; causes holds when the AHJ is on a different edition than the product documentation

---

## Where to go for more

- **FMP Alliance**: [fmpalliance.com](https://fmpalliance.com) — AHJ outreach, code documents, training
- **NFPA 70**: Article 726 (2023 NEC) / Article 722 (2026 NEC)
- [How FMP Is Installed](/guides/how-fmp-is-installed/) — installation steps and commissioning
- [Scoping and Estimating](/guides/scoping-and-estimating/) — pre-bid checklist and AHJ timeline planning
