---
title: "How FMP Is Installed: A Contractor's Overview"
description: "FMP installations follow Class 2 wiring methods — no conduit required — but the transmitter and receiver introduce commissioning steps and an AHJ documentation requirement that differ from conventional electrical work. Here's what to expect from rough-in through inspection."
summary: "FMP uses Class 2 wiring methods: route cable through existing pathways, terminate at receivers, commission the transmitter. The licensed electrician scope is limited to the panel connection. The main new steps are AHJ documentation and transmitter commissioning."
slug: how-fmp-is-installed
type: guides
weight: 40

knowledge_sources:
  - EXPL_FMP_ARCHITECTURE
  - CLAIM_DE_INSTALLATION_SCOPE_48_UNITS
  - CLAIM_FMP_CONDUIT_SIZING_RISER_RACEWAY
  - CLAIM_FMP_LABOR_SHIFT
  - OBJ_COMMON_CONTRACTOR
  - PROC_AHJ_DOCUMENTATION_CHECKLIST
  - CLAIM_CLASS4_VS_CLASS2_CLASS3
---

## Introduction

FMP installation looks unfamiliar the first time. The cable is small and light. There's no conduit on most of the run. The receivers at the far end are boxes you've never seen. The transmitter rack in the electrical room doesn't look like a panel.

Underneath that unfamiliar surface, the work is largely what low-voltage contractors already know: route cable, terminate pairs, label everything, commission the system. The electrician scope — connecting the transmitter to the existing AC panel — is a small portion of the total installation hours. The rest is low-voltage work.

This guide covers the full installation sequence, what's different from conventional electrical work, and what commonly goes wrong.

---

## System components

Every FMP installation has three parts:

**Headend (transmitter)**
Connects to an existing AC electrical panel. Manages fault monitoring for every power delivery cycle. Controls output to each cable run. The transmitter is the listed safety device — UL 1400-1. It is installed by a licensed electrician and is the only piece of the installation that touches line voltage.

**Managed power link (cable)**
Standard 16 AWG structured cable pairs — the same physical type used for communications wiring. No conduit required. No junction boxes along the run. The cable carries DC power packets from the transmitter to the receiver. It can share trays and raceways with low-voltage data cabling and cannot be mixed with line-voltage wiring.

**Load end (receiver)**
Converts the DC power packets to whatever the connected load needs: 240V AC for a heat pump, specific DC voltage for rack equipment, or other outputs depending on the receiver model. UL 1400-2 listed. In most jurisdictions, termination at the receiver does not require a licensed electrician — verify local amendments.

*The transmitter manages all safety behavior for the entire run. The cable and receiver have no protective function of their own — the safety logic lives in the headend.*

---

## What requires a licensed electrician

- **Panel connection at the transmitter input** — the transmitter connects to an existing AC panel; this is a line-voltage connection and requires a licensed electrician in all jurisdictions
- **Any line-voltage connection at the load** — for example, a heat pump disconnect fed from a conventional circuit that the project also includes
- **Permit application** — in most jurisdictions, the permit application requires a licensed electrician's signature

What typically does not require a licensed electrician (verify local amendments):
- Pulling and routing FMP cable
- Terminating at the receiver
- Mounting receivers and transmitters
- Commissioning the transmitter (operating the transmitter's commissioning check is not electrical work in the licensing sense)

FMP reduces the licensed electrician scope significantly compared to a conventional electrical retrofit. It does not eliminate it.

---

## Cable routing

FMP cable is routed using Class 2 installation methods. For contractors, this means the same techniques used for structured data cabling:

- **J-hooks and cable trays** — standard low-voltage support hardware
- **Plenum spaces** — use plenum-rated cable where required by code
- **Existing conduit (alongside low-voltage data cable)** — FMP cable may share conduit with Class 2 data cable; it may not share conduit with line-voltage wiring
- **Abandoned building risers** — in multifamily retrofit projects, abandoned steam, trash, laundry, and mail risers are the primary pathway; no new penetrations required in most buildings

**Conduit sizing, if conduit is used:**
- 4-inch conduit at 40% fill accommodates 8 cable pairs, delivering up to 144 kW of total capacity (at 1.5 kW per pair)
- 2-inch conduit is available for smaller applications
- The 40% fill ratio is required for code compliance and thermal management

**Routing constraints:**
- Check the manufacturer datasheet for maximum cable run length for your transmitter model — longer runs affect fault response time and transmitter sizing
- Keep FMP cable away from high-interference sources (motors, large AC circuits) if possible, though Class 4 cable is less sensitive than data cable on this point

---

## Termination

Termination at both ends is the same as structured cable termination:

- **At the transmitter**: terminate pairs to the output terminals per the transmitter manufacturer's diagram; each output port typically serves one cable run
- **At the receiver**: terminate pairs to the receiver input terminals; receivers are typically tool-terminated and require no special equipment

Label every run at both ends during termination. The transmitter's commissioning check will validate continuity and load presence before the system goes live — any mislabeled or swapped pair is caught at this step, not during inspection.

---

## Commissioning steps specific to FMP

These steps are in addition to standard low-voltage installation procedures:

1. **Set transmitter output parameters** — voltage, max current per port, zone configuration — per the manufacturer's commissioning guide for your specific transmitter model
2. **Run the transmitter commissioning check** — the transmitter validates cable continuity and receiver presence on each port before enabling power delivery; a failed port indicates an open, short, or misconfigured receiver
3. **Verify receiver output** — confirm the receiver is delivering the correct output voltage and current to the connected load; use a multimeter at the load connection point
4. **Document for the AHJ package** — record UL listing numbers (transmitter and receiver), cable lengths per run, and connected load specs; this goes into the permit package
5. **Simulated fault test** — many first-time AHJ inspections require a live demonstration of the transmitter's fault response; perform this with a simulated fault (typically a resistive load short) before the inspector arrives and be prepared to demonstrate it on site

---

## AHJ inspection for first-time jurisdictions

The first Class 4 installation in a jurisdiction that has not previously permitted one typically requires more inspector engagement than a repeat installation. Budget 30–60 minutes for a detailed walkthrough.

Inspectors will want to see:
- UL listing numbers on the transmitter and receiver (they may look them up independently)
- The one-line diagram and permit package reviewed in detail
- The transmitter's fault response — a simulated fault demonstration is common

Bring the OEM datasheet to the inspection. It should show max fault energy and fault response time. Inspectors unfamiliar with Class 4 often have questions about how the safety mechanism works; the datasheet is the authoritative reference.

For more detail on the permit package, see [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/).

---

## The labor picture

FMP shifts project cost from field labor to equipment. In a conventional electrical retrofit, the dominant cost line is the pathway work: conduit bending, core drilling, firestopping, pulling heavy cable through crowded risers. In an FMP installation, that work largely disappears — the cable is light, no conduit is required on most runs, and the terminations are fast.

The equipment cost — transmitters and receivers — replaces much of that field labor. On constrained retrofit projects with difficult pathways and high labor rates, this is a significant advantage. On short, simple runs with easy conduit access and low labor cost, the equipment cost can dominate and AC will likely win on price.

*The installation comparison is not cable vs. cable. It is the total cost of getting power to each endpoint — including pathway work, panel work, permitting, and schedule — using each approach.*

---

## Common mistakes

**Wrong NEC article on the permit** — citing Article 725 (Class 2/3) instead of Article 726 (2023) or Article 722 (2026). This causes immediate holds with AHJs unfamiliar with Class 4.

**Missing AHJ package elements** — submitting without UL listing numbers or without a safety model summary. In jurisdictions that haven't seen Class 4 before, the permit reviewer often doesn't know what to do with a one-line diagram that doesn't explain the safety logic.

**Exceeding cable run length spec** — the maximum cable run length depends on the transmitter model and the connected load; check the OEM datasheet before routing. Longer runs may require a different transmitter model or an intermediate receiver.

**Skipping the commissioning check** — the transmitter's commissioning check catches wiring errors before power delivery begins. Skipping it means faults discovered at inspection rather than during setup.

**Assuming termination requires an electrician** — in most jurisdictions it does not, but local amendments vary. Verify before assigning the termination scope.

---

## Related guides

- [NEC Class 4 / Article 726](/guides/nec-class-4-article-726/) — code article, AHJ documentation, permit checklist
- [Scoping and Estimating an FMP Project](/guides/scoping-and-estimating/) — cost drivers, ROM workflow, pre-bid checklist
- [Where FMP Fits](/guides/where-fmp-fits/) — qualification criteria and vertical use cases
