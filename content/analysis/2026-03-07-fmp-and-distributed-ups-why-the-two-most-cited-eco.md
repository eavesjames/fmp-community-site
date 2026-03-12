---
title: "FMP and Distributed UPS: Why the Two Most-Cited Economic Claims in Data Center Power Design Lack the Methodology to Be Used as Capital Budget Inputs"
date: 2026-03-07
draft: false
type: analysis
insight_id: "2026-03-07-A03"
levers: ["ups-resilience", "code-standards", "reliability-uptime", "monitoring-telemetry", "retrofits-mdus"]
which_verticals: ["data-centers"]
confidence: "High"
must_cite_items: ["40", "44", "100"]
---

## Thesis

The two economic claims most frequently cited in current data center power distribution discussions — Southland Industries' 'multi-million dollar savings' for FMP at 6MW scale (item 40) and AWS's '35% energy loss reduction' for distributed rack-level UPS (item 44) — share a critical evidentiary weakness: both are single-source, single-facility figures with undisclosed methodology. FMP savings omit AHJ approval timeline, commissioning soft costs, and supply chain lead time for DC components. The AWS efficiency figure does not specify its baseline (legacy vs. optimized centralized UPS), the rack density at which it was measured, or the runtime target. Practitioners using either figure directly in capital budgets or design decisions are accepting unquantified schedule and cost risk. This article would present the specific methodology gaps, quantify the risk range for each claim, and propose the evidence standard required before either figure can be used as a transferable engineering benchmark.

## Why this matters now

No single analyst connected the NFPA 855 retroactive enforcement trigger (item 46) directly to the BMS shutdown risk at short runtimes (item 100) as a combined forcing function toward distributed UPS architecture (item 44). Finance analyst treated them as separate cost buckets; MEP designer noted the overlap but did not quantify the convergence; compliance analyst flagged both but analyzed them in separate constraint buckets. The composite view is that the retrofit window created by NFPA 855 is the lowest-cost moment to also resolve the BMS discharge-rate problem — deferring one defers the other at increasing cost.

## Who should read this

data-center-owner-operator, mep-system-designer, compliance-ahj, electrical-contractor

## Article outline

1. H1: What the FMP cost comparison (item 40) actually claims and what it omits — parts-and-labor savings figure, missing soft costs (AHJ approval, commissioning labor, supply chain lead time, operational training), and the new-build vs. retrofit context dependency that is not disclosed in the webinar presentation.
2. H2: What the AWS efficiency claim (item 44) actually claims and what it omits — 35% loss reduction, missing baseline specification (which centralized UPS topology is the comparison?), missing rack density and runtime operating conditions, and the absence of third-party or non-AWS deployment validation.
3. H3: The risk of single-source figures becoming industry benchmarks — how both claims are propagating through analyst outputs and practitioner discussions as if validated, and what decisions are being made on that basis.
4. H4: The evidence standard required — what methodology disclosure, independent replication, and deployment context specification would be needed before either figure can be used as a capital budget input rather than a directional signal.

## Key questions for practitioners

- For the Southland Industries 6MW FMP comparison (item 40), can you obtain the full webinar recording and parts-and-labor breakdown? Specifically: does the savings figure include AHJ approval and commissioning costs, and is there a post-commissioning actual-vs-estimate comparison available?
- Has your organization received the AWS distributed UPS technical specification that underlies the 35% efficiency claim? Does AWS disclose the centralized UPS baseline, rack density, and runtime target for that figure, and is there a published deployment case study from a non-AWS facility?

## Evidence gaps

- Southland Industries full parts-and-labor breakdown from the item 40 webinar, itemized by component category (transformers, switchgear, conduit/pathways, labor), plus any post-commissioning actuals from the referenced 6MW facility.
- AWS technical publication or peer-reviewed source specifying the baseline topology, rack density, runtime target, and measurement methodology for the 35% efficiency gain claim in item 44.
- At least one non-AWS facility deploying distributed rack-level UPS with published TCO data including commissioning labor, monitoring infrastructure, and spare parts inventory costs.

## Must-cite items

- item 40
- item 44
- item 100
