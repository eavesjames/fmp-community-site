---
title: "The Oversizing Trap: How 3-Minute UPS Runtimes and NFPA 855 Compound to Make Every Battery Chemistry More Expensive"
date: 2026-03-06
draft: true
insight_id: "2026-03-06-A01"
status: "DRAFT"
levers: []
which_verticals: []
confidence: ""
must_cite_items: ["100", "46", "44"]
---

## Thesis

The data center industry's shift to 3-minute UPS runtimes was expected to reduce battery capex and floor space by leveraging faster generator failover. In practice, both battery chemistries require oversizing under short-runtime, high-current discharge profiles—lead-acid for energy density limits, lithium-ion to stay below BMS discharge-rate shutdown thresholds. NFPA 855 retroactive enforcement then applies compliance costs proportional to installed battery cabinet count, meaning the oversizing 'solution' amplifies the regulatory liability. No currently available chemistry provides a cost-optimal short-runtime UPS at scale; the distributed micro-UPS architecture (AWS model) may break the tradeoff but introduces operational prerequisites most non-hyperscale operators cannot meet without significant infrastructure investment.

## Why this is new

_Explain why this angle is original._

## Who cares

_Specify target audience._

## Recommended questions to research

- Do you have actual discharge current telemetry from generator failover tests that shows whether your lithium-ion BMS units are approaching or exceeding shutdown thresholds? If so, what oversizing factor did you deploy to create headroom?
- When you received your NFPA 855 compliance notice from the LA or NYC AHJ, what was the specific list of remediation items—was it hardware replacement, documentation submission, testing, or all three? What was the total cost and elapsed time from notice to final AHJ approval?
- If you are evaluating distributed rack-level UPS, what is the estimated annual cost of the monitoring infrastructure (DCIM integration, telemetry licensing, technician dispatch for hot-swaps) relative to the projected energy savings from the 35% conversion loss reduction?

## Evidence gaps to fill

- BMS discharge-rate threshold specifications (amperes per cell, total kW) from major lithium UPS OEMs (Saft, Samsung SDI, Eaton, Vertiv) to quantify the oversizing factor required to avoid shutdown.
- Actual peak discharge current measurements during generator failover events at operational data centers to determine how frequently facilities hit BMS thresholds in practice.
- Itemized NFPA 855 retrofit cost for a typical 250 kW–1 MW UPS installation (engineering, hardware, labor, testing, AHJ fees) from LA or NYC facilities that have completed compliance work.
- Third-party operational cost data for distributed rack-level UPS (non-AWS) deployments: DCIM integration hours, spare battery inventory carrying cost, technician dispatch frequency, MTTR vs. centralized baseline.
- Whether BMS threshold relaxation requires new UL 1973 or UL 9540 certification cycles, or can be achieved via firmware update within existing certifications.

## Must-cite items

- item 100: UPS Runtime Reduction: Battery Technology Trade-offs for Data Centers
- item 46: New NFPA 855 Battery Standard Could Impact Data Center UPS Designs
- item 44: AWS Designs In-Rack Micro UPS Units For a More Efficient Cloud
