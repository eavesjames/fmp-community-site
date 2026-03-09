---
title: "The Commissioning Gap: Why Short-Runtime UPS Claims Cannot Be Validated Under Current Acceptance Testing Practice"
date: 2026-03-09
draft: true
insight_id: "2026-03-09-A03"
status: "DRAFT"
levers: []
which_verticals: []
confidence: ""
must_cite_items: ["100", "46", "44"]
---

## Thesis

Data centers are purchasing and commissioning UPS systems with 3-5 minute runtime claims, but no standard commissioning test requires demonstration of nameplate runtime at nameplate discharge current under peak emergency load conditions. Lithium-ion BMS systems can deliver rated kWh capacity at moderate discharge rates but will trigger automatic shutdown at the high discharge currents required by short-runtime failover scenarios. AHJs in LA and NYC are enforcing NFPA 855 without a published standard for witnessed UPS runtime testing at peak discharge. The result is a systematic gap between purchased UPS capability and actual emergency performance that will not surface until a real outage, and that NFPA 855 enforcement is about to force operators to confront through commissioning documentation requirements they are not currently meeting.

## Why this is new

_Explain why this angle is original._

## Who cares

_Specify target audience._

## Recommended questions to research

- In your last UPS commissioning acceptance test, was the system tested at 100% nameplate discharge current for the full rated runtime duration with a third-party witness, or was acceptance based on manufacturer certification and partial load testing?
- Have your UPS vendors disclosed the BMS discharge current threshold at which automatic shutdown triggers, and have you verified that this threshold is not exceeded by your actual peak load during generator transfer?

## Evidence gaps to fill

- Existing UPS commissioning test standards (IEEE 1188, NFPA 110 Section 8) and whether any require high-rate discharge testing at nameplate current — needed to confirm or refute the commissioning gap claim.
- Lithium BMS discharge current thresholds from major UPS battery vendors (Saft, CATL, EnerSys, LG) compared against typical data center failover discharge current profiles at 3-minute runtime — the quantitative data needed to assess how often BMS shutdown would trigger in practice.
- Any AHJ enforcement actions or design review rejections citing UPS runtime non-performance in LA or NYC post-NFPA 855 enforcement — field evidence that the commissioning gap has already produced AHJ friction.

## Must-cite items

- item 100: UPS Runtime Reduction: Battery Technology Trade-offs for Data Centers
- item 46: New NFPA 855 Battery Standard Could Impact Data Center UPS Designs
- item 44: AWS Designs In-Rack Micro UPS Units For a More Efficient Cloud
