---
title: "One Gap, Two Technologies: Why PoE and Class 4 FMP Need a Unified Commissioning Standard Before AHJ Delays Kill Edge Power Consolidation"
date: 2026-02-27
draft: true
insight_id: "2026-02-27-A03"
status: "DRAFT"
levers: []
which_verticals: []
confidence: ""
must_cite_items: ["36", "55"]
---

## Thesis

Power over Ethernet (item 55) and NEC Class 4 fault-managed power (item 36) are architecturally converging on the same design pattern — centralized low-voltage DC distribution with infrastructure-level UPS backup and remote power management — but are being standardized, inspected, and commissioned as if they are unrelated technologies. Both lack AHJ-approved commissioning procedures, published redundancy standards for mission-critical OT applications, and contractor training programs. The result is that practitioners choosing between PoE and FMP for edge OT applications are making an uninformed architectural bet, and AHJs are inventing inspection criteria independently for each. A unified commissioning and inspection framework covering centralized low-voltage DC power distribution — regardless of implementation technology — would eliminate duplicated standards development effort and reduce AHJ review cycles for both technologies simultaneously.

## Why this is new

_Explain why this angle is original._

## Who cares

_Specify target audience._

## Recommended questions to research

- Have you deployed both PoE and Class 4 FMP in the same facility or portfolio? If so, what drove the technology choice for each application, and did AHJ inspection timelines or outcomes differ between the two?
- For your PoE-powered OT devices, do you have N+1 PSE redundancy designed in? If a PoE switch fails, what is your recovery procedure and SLA, and has that procedure been reviewed by your AHJ?

## Evidence gaps to fill

- Failure mode data for PoE PSE/switch failures in industrial and commercial OT environments — mean time between failures, downstream device impact scope, recovery time — to establish the reliability baseline that a redundancy standard must address
- AHJ survey data: average review time and resubmittal rate for Class 4 FMP permit submissions vs. PoE system submissions in commercial and industrial applications — to quantify the current inspection delay cost
- Published failure incident reports for Class 4 FMP installations (if any exist) to establish a field safety record for the technology
- IEEE P802.3 or NFPA working group status on PoE redundancy standards for life-safety and OT applications — to determine whether a unified framework is being developed or whether the gap is genuinely unaddressed

## Must-cite items

- item 36: NEC Code Questions on LED Lighting: Class 2, 3, and Class 4 Fault Managed Power
- item 55: Integrating PoE into Android-Based Single Board Computers for Industrial Edge
