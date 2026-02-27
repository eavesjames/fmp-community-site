---
title: "What Is Fault Managed Power (Digital Electricity)?"
description: "A clear, grounded explanation of how FMP works, what problem it solves, how it differs from PoE and conventional wiring, and where it fits — for practitioners and informed newcomers."
summary: "FMP makes power safe through continuous monitoring, not through insulation or power limiting. The result: safe delivery of kilowatts through standard structured cable, without conduit or service upgrades."
slug: what-is-fmp
type: guides
weight: 10

knowledge_sources:
  - CLAIM_DIGITAL_ELECTRICITY_MECHANISM
  - EXPL_FMP_ARCHITECTURE
  - MAP_AC_VS_FMP_FEATURES_COMPARISON
  - MAP_TRADITIONAL_ELECTRICAL_VS_DE_HEAT_PUMP_RETROFIT
  - CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS
  - CLAIM_IDEAL_BUILDING_CHARACTERISTICS_HEAT_PUMP_RETROFIT
  - CLAIM_DE_INSTALLATION_SCOPE_48_UNITS
  - CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY
  - RULESET_FMP_FIT_CONDITIONS
  - CLAIM_CLASS4_VS_CLASS2_CLASS3
  - CLAIM_NEC_ARTICLE_722_TRANSITION
  - PROC_AHJ_DOCUMENTATION_CHECKLIST
  - Digital_Edge_Belden.yaml
  - what_is_de.yaml
  - low_disruption_AI_racks.yaml
  - DATA_RES_DATA_CENTER_DISTRIBUTION_AC_VS_FMP_INSTALLED_COST_TABLE1_2024
---

## Introduction

Most electrical infrastructure improvements follow the same script: bigger panels, heavier conduit, longer permitting queues, and eventually a service upgrade that costs tens of thousands of dollars and takes a year or two to complete. That script works fine for greenfield construction. It's a serious problem everywhere else.

Fault Managed Power (FMP) — also marketed commercially as **Digital Electricity (DE)** by VoltServer — is a power delivery technology that skips most of that script. It routes kilowatts through standard structured cable, using the same installation methods allowed for low-voltage data wiring, and without requiring panels, conduit, or service upgrades at the remote end.

This article explains how it works, what makes it different, and where it actually fits. It is not a sales document. Where claims are grounded in sourced knowledge files, they're marked as such. Where something is synthesis or inference, it's said so.

---

## What DE / FMP is

FMP delivers power as packetized DC: the transmitter sends rapid bursts of high-voltage DC over standard structured cable, and each burst is checked against fault conditions before the next one fires. [CLAIM_DIGITAL_ELECTRICITY_MECHANISM] The key safety claim — grounded in how Class 4 differs from Class 2 and Class 3 under the NEC — is this: FMP does not limit *how much power it can deliver*; it limits *how much energy a fault can accumulate before being stopped*. [CLAIM_CLASS4_VS_CLASS2_CLASS3, what_is_de.yaml] That distinction is everything.

Here's how it works in practice [CLAIM_DIGITAL_ELECTRICITY_MECHANISM]:

1. A **transmitter** connects to an existing AC electrical panel and converts that AC to packetized DC — rapid bursts of high-voltage DC power, each checked against a set of safety conditions before the next burst is sent.
2. **FMP cable** — standard 16 AWG structured cable pairs, the same physical type used for communications wiring — carries these bursts from the transmitter to wherever power is needed. No conduit required. No junction boxes along the run.
3. A **receiver** at the far end converts the bursts back into the form the connected load needs: 240V AC for a heat pump, or a specific DC voltage for rack equipment or edge devices. [EXPL_FMP_ARCHITECTURE]

The safety mechanism lives entirely in the transmitter. It monitors every power packet and shuts down the circuit if it detects a fault condition — touch fault, short circuit, ground fault, or arc fault. The shutdown happens in under 2 milliseconds, which is faster than human nerve response time.

*Synthesis: The phrase "packetized DC" is accurate but often misleading. It makes FMP sound like data networking with electricity bolted on. The physics is different: what's being sent is real high-voltage DC power, not information signals. The "packet" framing describes the monitoring cycle — each burst is checked before the next fires — not a fundamentally different transmission medium.*

---

## What problem it solves

FMP addresses two related but distinct problems.

**Problem 1: The electrical upgrade barrier in retrofit buildings**

Getting heat pumps, induction cooking, or other electric loads into older multifamily buildings requires electrical capacity those buildings don't have. The conventional path — upgrading the panel, the feeders, and often the utility service — costs approximately **$20,000 per unit**, takes **up to two years** (including utility coordination), and forces residents out during major work. According to industry data cited in the knowledge files, **roughly 50% of heat pump retrofit projects in older buildings are canceled because of these costs alone**. [CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS]

The target building profile for this problem: pre-1973 construction, 40A electrical panels, failing or aging hydronic heating systems, absorption chillers — buildings where the electrical infrastructure is simultaneously inadequate and expensive to upgrade, and where the building envelope provides no easy path for new conduit. [CLAIM_IDEAL_BUILDING_CHARACTERISTICS_HEAT_PUMP_RETROFIT]

FMP changes the math. Instead of upgrading the electrical service and running new branch circuits to every unit, a single transmitter rack connects to the existing service at the electrical room. Structured cable runs through whatever pathways already exist — abandoned steam risers, trash chutes, laundry chutes, mail chutes — and receivers terminate at each unit. Cost per unit drops to approximately **$500–600/drop** versus $20,000 for the conventional path. [MAP_TRADITIONAL_ELECTRICAL_VS_DE_HEAT_PUMP_RETROFIT]

*That's a 95%+ cost reduction. Take that number as directional, not guaranteed — actual costs vary by building configuration, riser conditions, and local labor. But the order of magnitude is sourced from a published deck and supported by multiple case references in the knowledge files.*

**Problem 2: Distributed power at scale**

In data centers, the problem is different but structurally similar: too much power needed at too many points, with distribution infrastructure that wasn't built for current load densities. Average AI server rack density has reached approximately 27 kW (per AFCOM 2025, cited in site pulse content), well above what most existing busway and PDU specifications were designed for.

FMP cable runs in the same trays as data cabling. There's no intermediate distribution switchgear at the rack row. In a 6 MW data center reference scenario, FMP distribution runs approximately $13.4 million installed versus $19.9 million for equivalent conventional AC distribution — a savings of $6.6 million, or 32.9%. [DATA_RES_DATA_CENTER_DISTRIBUTION_AC_VS_FMP_INSTALLED_COST_TABLE1_2024]

---

## How it differs from conventional electrical distribution

The table below captures the directional differences. These are generalizations; specific tradeoffs vary by application. [MAP_AC_VS_FMP_FEATURES_COMPARISON]

| Attribute | Traditional AC | Fault Managed Power |
|---|---|---|
| Cable | Larger gauge; conduit and busway typically required | 16 AWG structured cable pairs; typically no conduit required |
| Pathway | Conduit fill, core drilling, firestopping, crowded risers are cost drivers | Still needs planning, but fewer hard pathway constraints per run |
| Remote-end protection | Branch circuits + breakers; panel schedules drive layout | Protection handled at transmitter; no downstream panel required |
| Commissioning | Power and controls often separate trades | Integrated monitoring; faults localize more easily |
| Adding capacity later | Late changes often trigger disruptive rework | Adding endpoints can be as simple as running another cable |
| Labor vs. equipment balance | More field labor in routing, pulling, and terminations | Less field labor; cost concentrated at centralized equipment |

The practical consequence: FMP shifts effort from distributed field work — conduit bending, panel scheduling, permits at each location — to a centralized equipment install. On a clean greenfield site with easy conduit access and cheap labor, that's not obviously better. On a retrofit in an occupied building with no clear pathways and an 18-month permitting queue, it can change whether the project happens at all.

---

## How it differs from PoE, Class 2, and standard DC framing

This is where most confusion arises, and where the distinction matters most for practitioners.

**Class 2 and Class 3 circuits** (NEC Article 725) are made safe by limiting total output power. The circuit cannot output enough energy to cause a shock or start a fire even in a fault condition — because the output is capped too low. PoE (Power over Ethernet) works on this principle. IEEE 802.3bt Type 4 — the most powerful standard PoE — tops out at 71 W over a 100 m run.

**Class 4 / FMP** (NEC Article 726) is made safe differently. The output is *not* power-limited — the transmitter can deliver kilowatts. Safety comes from the monitoring cycle: faults are detected and stopped before energy accumulates to a harmful level. [CLAIM_CLASS4_VS_CLASS2_CLASS3]

The practical comparison, from published performance data [Digital_Edge_Belden.yaml]:

| System | Max power | Max range at that power |
|---|---|---|
| PoE (IEEE 802.3bt Type 4) | 71 W | 100 m |
| 48V DC (standard) | ~80–90 W | 123–247 m |
| Fault Managed Power | ~1,500 W | ~180 m |
| Fault Managed Power | ~170 W | 2,000+ m |

FMP is not "PoE at higher wattage." It's a different safety architecture that happens to use similar cable and similar installation methods. The cable doesn't care. The safety logic is entirely different. A Class 2 system is safe because it's weak. A Class 4 system is safe because it's fast — fast enough to stop a fault before it becomes dangerous.

*Synthesis: The "it's just DC" framing you'll sometimes hear is also incomplete. Standard DC distribution (48V, 380V, 800V busway systems) uses conventional protection methods — fusing, breakers, arc-flash protective gear. FMP doesn't require arc-flash protective equipment because the transmitter eliminates the arc-flash condition itself. That's a meaningful operational difference, not just a marketing claim — it changes what trades can work on the cable and under what conditions.*

---

## Code and compliance framing

FMP has a specific place in the National Electrical Code. Getting this right matters for permit submissions.

**Class 4 is not Class 2.** This is the most common early mistake. Installers familiar with low-voltage work sometimes cite Article 725 (the Class 2 / Class 3 article) for FMP installations. The correct article is Article 726 in the 2023 NEC. In the 2026 NEC, it's been renumbered to Article 722 — the safety model is unchanged, only the article number changed. [CLAIM_NEC_ARTICLE_722_TRANSITION]

During the transition period when different jurisdictions are on different code editions, permit packages should cite both: *"Article 726 (2023 NEC) / Article 722 (2026 NEC)."* An AHJ on the 2023 edition may not recognize 722; one on 2026 may not recognize 726 in older product documentation.

**What Class 4 allows:** FMP uses Class 2 installation methods — no conduit required, flexible routing, cable trays, J-hooks, plenum spaces — while delivering far more power than Class 2 circuits can carry. The transmitter is the listed safety device. The cable is not the limiting factor.

**Permitting for a first-time jurisdiction:** A complete AHJ package for a first-time Class 4 installation includes: [PROC_AHJ_DOCUMENTATION_CHECKLIST]

1. UL listing numbers for the transmitter (UL 1400-1) and receiver (UL 1400-2)
2. NEC article citation — both editions during the transition
3. A safety model summary: how fault detection works, max fault energy, response time (under 2 ms)
4. A one-line diagram: panel → transmitter → cable → receiver → load
5. Contact information for AHJ questions (FMP Alliance or NFPA)

Budget 2–4 additional weeks for inspector education on the first project in a new jurisdiction. Inspectors will typically want to see the transmitter's fault response demonstrated with a simulated fault. Repeat projects in the same jurisdiction move significantly faster.

*Knowledge gap: the YAML knowledge files do not contain a complete code-adoption map by state or jurisdiction. Whether a given jurisdiction has adopted the 2023 or 2026 NEC is critical for permit language, and that information is not in the current knowledge base. Check with the FMP Alliance or NFPA directly.*

---

## Where it fits best

FMP is strongest when conventional wiring is pathway-constrained, schedule-constrained, or blocked by a required service upgrade. It is not a universal replacement for conventional electrical distribution. [RULESET_FMP_FIT_CONDITIONS]

**Strong fit:**
- Long cable runs where conduit and branch-circuit buildout become expensive and slow
- Retrofits in occupied buildings where pathway access is constrained and disruption is costly
- Projects where speed to operation is a significant value driver
- Distributed endpoints — many loads across a large floor plate or building stack — that benefit from repeatable, standardized drops
- Situations where avoiding a service upgrade is the key to project viability

**Weak fit:**
- Short, simple runs with easy conduit access and low field labor cost
- Greenfield construction with abundant pathway space designed in from the start
- A single very large load at one location (FMP aggregates many drops; it doesn't compete with a single large AC feeder)
- Sites where the transmitter headend location is infeasible — no panel access, no rack space, no suitable electrical room

*Synthesis: The fit question is best framed not as "is FMP cheaper than wire?" but as "what is the total cost — material, labor, permits, service upgrades, schedule delay, and disruption — of getting power to this location the conventional way?" FMP doesn't win on commodity wiring cost. It wins when the total conventional path is expensive or infeasible.*

---

## Practical installation and scoping implications

**What a 48-unit building retrofit looks like** [CLAIM_DE_INSTALLATION_SCOPE_48_UNITS]:

1. Build a 19-inch rack and mount 6 transmitters (400A, 208V AC, 3-phase input)
2. Terminate 96 pairs of 16 AWG wire to the transmitter output terminals
3. Run 12 eight-pair cables through the building — using abandoned trash, laundry, mail, or steam risers if available
4. Terminate 2 pairs per receiver at each unit; receiver outputs 240V AC for the heat pump

That's the full scope of the FMP-specific work. The licensed electrician work is the panel connection at the transmitter input. The rest uses low-voltage installation methods.

**Conduit capacity, if conduit is used** [CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY]:

- 4-inch conduit at 40% fill, 8 pairs at 1.5 kW per pair = 144 kW delivered capacity
- 2-inch conduit available for smaller applications
- The 40% fill ratio applies for code compliance and thermal management

**The scoping inputs you need before pricing:**
- How many endpoints (each load = one receiver)
- What abandoned pathways exist — risers, chases, ceiling cavities
- Distance from the electrical room to the farthest endpoint (affects transmitter sizing and cable run)
- Which NEC edition the jurisdiction has adopted
- Whether this is the first Class 4 installation in this jurisdiction (adds permitting timeline)

---

## Common misconceptions

**"It's PoE at higher wattage."**
No. PoE and FMP use different safety architectures. PoE is safe because it can't output enough energy to harm. FMP is safe because it stops faults before they accumulate harmful energy. The installation method looks similar; the underlying physics is different. Confusing the two leads to incorrect code citations (Article 725 vs. Article 726) and incorrect assumptions about what the cable can handle.

**"It eliminates the need for a licensed electrician."**
Partially true, and the "partially" matters. The transmitter connects to an existing electrical panel — that connection requires a licensed electrician in all jurisdictions. Termination at the receiver end may not require a licensed electrician (this varies by jurisdiction and local amendments). The permit application typically requires a licensed electrician's signature. FMP reduces the total licensed electrician scope; it doesn't eliminate it.

**"It works anywhere conventional wiring works."**
FMP has specific fit conditions (see above). It's not always cheaper, and it's not always the right tool. On a short run with easy conduit access in a new building, conventional AC will likely be faster and cheaper. FMP's advantage is concentrated in constrained retrofits and long-run distributed loads.

**"No permits required because it's low-voltage."**
FMP uses low-voltage installation methods but it is not a low-voltage system in the regulatory sense. It's Class 4 under the NEC and requires a permit in most jurisdictions. The permit process is what requires the AHJ documentation package described above.

**"The transmitter replaces the panel."**
The transmitter connects *to* the existing panel — it doesn't replace it. What gets eliminated is the panel at the *remote end*: no subpanel required in the tenant space or data center row. The building's main electrical service and its panels remain in place.

---

## Conclusion

Fault Managed Power is best understood as a different safety architecture, not a different wiring material. Conventional power is safe because faults are controlled after the fact — by insulation, breakers, and protective devices that interrupt current once a hazard develops. FMP is safe because faults are stopped before the fact — by a transmitter that monitors every power packet and shuts down in under 2 milliseconds if something goes wrong.

That architectural difference is what allows FMP to use Class 2 installation methods — standard structured cable, no conduit, flexible routing — while delivering power levels that Class 2 circuits can never reach.

Where it matters most is in the gap between "this project needs power" and "this project can afford what conventional electrical would cost." For a first-time visitor, the most useful frame is this: FMP doesn't make electrical distribution cheap. It makes electrical distribution *possible* in places where the conventional approach has become impractical.

---

## knowledge_sources

**Tier 1 knowledge blocks (structured YAML blocks with IDs):**

| Block ID | What it grounded in this article |
|---|---|
| `CLAIM_DIGITAL_ELECTRICITY_MECHANISM` | How the transmitter, cable, and receiver work; 1K+ installation count; mechanism description |
| `EXPL_FMP_ARCHITECTURE` | Three-component system model (headend, link, receiver) |
| `MAP_AC_VS_FMP_FEATURES_COMPARISON` | AC vs FMP feature comparison table |
| `MAP_TRADITIONAL_ELECTRICAL_VS_DE_HEAT_PUMP_RETROFIT` | $20K/unit vs $500–600/drop comparison; scope of work; timeline |
| `CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS` | $20K/unit, 2 years, 50% cancellation rate |
| `CLAIM_IDEAL_BUILDING_CHARACTERISTICS_HEAT_PUMP_RETROFIT` | Pre-1973, 40A panel, hydronic/absorption chiller target profile |
| `CLAIM_DE_INSTALLATION_SCOPE_48_UNITS` | 48-unit installation: 4 steps, transmitter count, cable specs, riser pathway types |
| `CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY` | 4-inch conduit at 144 kW, 40% fill, 8 pairs at 1.5 kW/pair |
| `RULESET_FMP_FIT_CONDITIONS` | Favorable and unfavorable conditions for FMP deployment |
| `CLAIM_CLASS4_VS_CLASS2_CLASS3` | Class 2/3 vs Class 4 safety architecture distinction |
| `CLAIM_NEC_ARTICLE_722_TRANSITION` | Article 726 (2023) → Article 722 (2026) renumbering |
| `PROC_AHJ_DOCUMENTATION_CHECKLIST` | AHJ permit package contents |

**Tier 2 document sources (extracted white papers and published articles):**

| File | What it grounded |
|---|---|
| `Digital_Edge_Belden.yaml` | PoE vs DC vs FMP performance comparison table (71 W @ 100 m vs 1,500 W @ 180 m); UL 1400-1 / UL 1400-2 standard references |
| `what_is_de.yaml` | Pulse cycle timing (2.0 ms cycle, 1.5 ms on, 0.5 ms gap), 336V HVDC voltage, fault types monitored |
| `low_disruption_AI_racks.yaml` | 500 packets/second; 80% overhead space reduction for AI rack deployments |
| `DATA_RES_DATA_CENTER_DISTRIBUTION_AC_VS_FMP_INSTALLED_COST_TABLE1_2024` | $13.4M (DE) vs $19.9M (AC) for 6 MW data center; $6.6M / 32.9% savings |

**Known gaps in the current knowledge base:**

- No YAML block covers jurisdiction-by-jurisdiction NEC code adoption status — critical for permit planning
- No YAML block covers the distinction between VoltServer-specific DE products and the broader FMP/Class 4 ecosystem (Cence Power, Panduit, Southwire, etc.)
- `CLAIM_FMP_DEFINITION` (`confidence: medium`, `source_id: SRC_TBD`) was removed from this article's grounding. The definitional substance it contained has been re-grounded in `CLAIM_DIGITAL_ELECTRICITY_MECHANISM`, `CLAIM_CLASS4_VS_CLASS2_CLASS3`, and `what_is_de.yaml`. The block should be fixed in the knowledge base — add a canonical source (NEC Article 726, FMP Alliance technical brief, or a UL standard reference) and promote confidence to high before re-introducing it as a citable block in any article.
