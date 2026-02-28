---
title: "Scoping and Estimating an FMP Project"
description: "How to qualify an FMP project, build a reliable ROM estimate, and identify the cost drivers that determine whether FMP wins against conventional AC. Covers the seven-step ROM workflow, pre-bid data requirements, and AHJ timeline planning."
summary: "FMP project cost is driven by endpoint count, run length, and pathway access — not by conduit or service upgrades. Here's how to qualify a project quickly, build a ROM estimate, and know when AC will likely win."
slug: scoping-and-estimating
type: guides
weight: 50

knowledge_sources:
  - PROC_FMP_ESTIMATING_ROM
  - CHK_FMP_FIELD_QUALIFICATION
  - MAP_TECH_TO_OWNER_VALUE
  - CLAIM_FMP_LABOR_SHIFT
  - RULESET_FMP_FIT_CONDITIONS
  - CLAIM_ELECTRICAL_UPGRADE_BARRIER_HEAT_PUMPS
  - CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY
  - CLAIM_IDEAL_BUILDING_CHARACTERISTICS_HEAT_PUMP_RETROFIT
---

## Introduction

Estimating an FMP project starts with a different set of inputs than a conventional electrical estimate. There is no conduit schedule. There is no panel schedule at the remote end. There is no service upgrade line item. Instead, the estimate is built from endpoint count, run length, pathway method, headend build, and commissioning scope.

This guide covers how to determine whether a project belongs in the FMP column at all, how to build a reliable rough-order-of-magnitude (ROM) estimate once it does, and what data you need to collect before you can price it.

---

## Step 1: Qualify before estimating

Not every project is an FMP project. Before investing in detailed estimating, use the six-question field qualification:

1. **Is this a retrofit with pathway or riser constraints?**
2. **Are run lengths long, or is routing complex** — firestopping, asbestos, structural issues?
3. **Is speed to market valuable** — does downtime or tenant disruption have a real cost?
4. **Are there many endpoints** where repeatable, standardized drops would reduce per-unit cost?
5. **Would AC require panel upgrades, new risers, or heavy conduit work?**
6. *(Counter-check)* **Is this a short, simple run with cheap labor** — does AC likely win?

**If three or more of questions 1–5 are yes, treat the project as an FMP candidate and proceed to ROM estimating.** A strong yes to question 6 is a signal to stop and check whether the conventional path is actually cheaper before proceeding.

FMP wins on constrained retrofits, long runs, distributed endpoints, and projects where the conventional path is blocked by cost or schedule. It does not win on commodity wiring jobs.

---

## Step 2: The ROM estimating workflow

A reliable ROM estimate has seven elements. Work through them in order — each step informs the next.

**1. Define loads and endpoints**
Count the number of receivers required — each load (heat pump unit, rack, cabinet, device) needs one receiver. Record the required power per endpoint in kW. This is the primary driver of transmitter capacity and the primary material cost line.

**2. Define topology**
Identify headend location(s): where the transmitter rack goes, which panel it connects to, how many channels or ports are needed, and whether any redundancy is required. The headend location determines the transmitter model and the longest cable run.

**3. Run-length model**
Measure or estimate average and maximum cable run lengths from the headend to each endpoint. Choose the pathway method for each segment: J-hooks and cable trays, open tray, existing conduit (alongside low-voltage data cable), or new conduit. Run length and pathway method are the primary labor drivers.

**4. Termination count**
Count terminations: both ends of each cable run, plus any intermediate pull points. Multiply by labor time per termination. Include labeling and testing time — this is where estimates most often undercount.

**5. Headend labor**
Estimate the work to build the transmitter rack: rack mounting, AC panel feed, cable dressing, transmitter configuration, documentation. This is licensed electrician work and should be scoped separately.

**6. Commissioning and testing**
Estimate the transmitter commissioning check, per-port verification, punch list time, and any support calls during initial startup. For first-time jurisdictions, add time for the AHJ inspection and any simulated fault demonstration.

**7. Compile and output**
Assemble the BOM (transmitters, receivers, cable, hardware) and the labor hours by task. Output a ROM total with explicit assumptions — pathway method assumed, run lengths assumed, AHJ timeline assumed. Flag any items where the assumption could be wrong by more than 20%.

---

## Primary cost drivers

| Driver | Why it matters |
|---|---|
| Endpoint count | Each load needs a receiver — this is the primary material cost line |
| Run length and pathway complexity | Longer runs require a larger transmitter; complex pathways drive labor cost |
| Termination count and labor rate | Terminations at both ends of every run; labor rate varies significantly by market |
| Headend build complexity | Larger transmitter racks, redundancy requirements, and documentation scope all add cost |
| Commissioning and testing scope | First-time jurisdictions add inspection time; complex topologies add validation time |
| AHJ familiarity | First Class 4 permit in a jurisdiction adds 2–4 weeks to schedule |

---

## What FMP eliminates from the conventional cost model

In a conventional electrical retrofit, the following line items are standard. In an FMP project, most or all of them disappear:

- **Service upgrade** — typically the largest single cost item in a multifamily retrofit; $10,000–$30,000 or more depending on utility and switchgear scope; FMP avoids it entirely by working within the existing service
- **Panel upgrade** — $5,000–$15,000 per tier; eliminated because there is no subpanel at the remote end
- **Conduit material and labor** — significant in pre-1973 buildings with constrained pathways; eliminated on most runs because FMP uses Class 2 installation methods
- **Permit delays from utility queue** — 6–18 months in many markets; eliminated because no utility service work is required

*Eliminating the service upgrade is typically the biggest driver of FMP's cost advantage on multifamily retrofit projects. On a 40-unit building, avoiding a $20,000-per-unit conventional upgrade can represent hundreds of thousands of dollars in project savings — even if the FMP equipment and installation costs are higher than simple cable cost.*

---

## Transmitter sizing rules of thumb

- **Residential heat pump unit**: approximately 5–12 kW nameplate load; a single transmitter serves multiple units depending on model capacity
- **Data center rack at AI density**: average 27 kW per rack (AFCOM 2025); transmitter selection driven by per-port capacity and number of ports
- **Cable capacity**: at 1.5 kW per cable pair, 8 pairs in a 4-inch conduit (40% fill) delivers 144 kW of total capacity
- **Run length limit**: maximum cable run length depends on the transmitter model and connected load — check the OEM datasheet before routing; longer runs may require a different transmitter model

Always check the OEM datasheet for the specific transmitter model. Nameplate kW at the load is not the same as the transmitter output requirement — factor in efficiency of the receiver and cable losses.

---

## Pre-bid data checklist

Before pricing an FMP scope, collect:

- **Riser and pathway survey** — which pathways are available and clear; which have fire-stop penetrations requiring rework; whether abandoned risers are accessible and usable
- **Panel location and capacity** — the transmitter connects to an existing panel; distance from the panel to the headend location affects conduit and cable labor; confirm the panel has capacity for the transmitter feed
- **Load schedule** — connected devices and nameplate kW for each endpoint; this determines transmitter sizing and BOM
- **Endpoint locations and distances** — floor plan or as-built with endpoint locations; measure or estimate cable run lengths from the headend
- **AHJ research** — has this jurisdiction permitted a Class 4 installation before; which NEC edition have they adopted (2020, 2023, or 2026 — this affects permit document language)
- **First-time jurisdiction flag** — if this is the first Class 4 permit in the jurisdiction, add 2–4 weeks to the schedule and plan for additional inspector documentation

---

## Schedule considerations

On a conventional electrical retrofit, the longest schedule driver is often utility coordination for the service upgrade — 6–18 months in many markets. FMP eliminates this. The longest schedule driver on an FMP project is typically the first-time AHJ education process if the jurisdiction has not previously permitted Class 4.

For repeat installations in a jurisdiction that has already permitted Class 4, the permit process is similar in timing to any other low-voltage permit. For first-time jurisdictions, the AHJ education step is real and should be planned for, not optimized away from the schedule.

For permit package requirements, see [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/).

---

## The cost comparison frame

FMP project cost is not directly comparable to conduit-and-wire cost on a per-foot or per-unit basis. The right comparison is the total cost of getting power to each endpoint using each approach — including all of the following:

- Material (cable, equipment, conduit if required)
- Field labor (routing, termination, commissioning)
- Licensed electrician scope (panel connection, permit)
- Permit costs and timeline (including service upgrade queue if applicable)
- Disruption cost (occupant relocation, downtime, lost revenue)

When the conventional path requires a service upgrade, new risers, and disruptive pathway work in an occupied building, FMP's equipment cost premium is frequently smaller than the conventional path's labor, service upgrade, and disruption costs combined.

When the conventional path is a short conduit run in a new building with cheap labor and no service upgrade, FMP's equipment cost is not justified.

---

## Related guides

- [Where FMP Fits](/guides/where-fmp-fits/) — qualification criteria and vertical use cases
- [How FMP Is Installed](/guides/how-fmp-is-installed/) — installation steps, commissioning, and common mistakes
- [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/) — code article, AHJ documentation, and permit timeline
