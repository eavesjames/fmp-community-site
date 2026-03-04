---
title: "One Gap, Two Technologies: Why PoE and Class 4 FMP Need a Unified Commissioning Standard"
description: "Power over Ethernet and NEC Class 4 Fault Managed Power are converging on the same architectural pattern — centralized low-voltage DC distribution with remote power management — but are being standardized, inspected, and commissioned as if they are unrelated technologies. A unified commissioning framework would reduce AHJ review cycles and improve field outcomes for both."
summary: "PoE and Class 4 FMP solve the same architectural problem from different directions. They share no commissioning standard, no inspection framework, and no contractor training pathway. The cost of that divergence falls on AHJs, installers, and building owners — and is avoidable."
slug: one-gap-two-technologies
date: 2026-02-27
draft: true
type: originals

insight_id: "2026-02-27-A03"

knowledge_sources:
  - CLAIM_FMP_DEFINITION
  - CLAIM_CLASS4_VS_CLASS2_CLASS3
  - CLAIM_NEC_ARTICLE_722_TRANSITION
  - PROC_AHJ_DOCUMENTATION_CHECKLIST
  - MAP_DE_VS_POE_DC_PERFORMANCE
---

## The convergence nobody is talking about

Power over Ethernet (PoE) and NEC Class 4 Fault Managed Power (FMP) are usually discussed as separate technologies aimed at separate applications. PoE powers network-connected devices — cameras, access points, sensors, LED lighting controllers — at 48V DC over ethernet cable. Class 4 FMP powers high-wattage loads — heat pumps, EV chargers, edge compute, appliances — at approximately 350V DC over structured cable.

They are different in voltage, power range, and target application. But they are converging on the same design pattern:

- **Centralized power source** (PoE switch or FMP transmitter) that manages the circuit from one point
- **DC distribution** over existing or new low-gauge structured cable, without conduit
- **Remote monitoring and control** of power delivery to each endpoint
- **Infrastructure-level backup** at the centralized source rather than at each device
- **Reduced installation complexity** relative to conventional branch circuits

This convergence is architectural, not coincidental. Both technologies are responses to the same underlying reality: buildings contain increasingly distributed loads that need individually managed power, and running a branch circuit to each load is too expensive and too disruptive to execute at scale.

*Synthesis: The convergence matters because it means PoE and Class 4 FMP will increasingly compete for the same applications in the 50–300W range, and will increasingly be deployed together in the same buildings. The question of how they are commissioned, inspected, and trained for is not an academic question — it determines how fast either technology can be adopted.*

---

## Where they diverge in practice

Despite architectural convergence, the two technologies are treated as completely separate domains by every stakeholder involved in the commissioning and inspection process.

**AHJ inspection:** PoE-powered systems are generally not inspected at all — IEEE 802.3 PoE is a Class 2 circuit under the NEC, which means it does not require an electrical permit in most jurisdictions. Class 4 FMP circuits require a permit under NEC Article 726, but AHJs vary widely in their familiarity with that article. Some jurisdictions treat Class 4 submittals as routine; others invent inspection criteria on the fly because the inspector has never reviewed a Class 4 project.

**Redundancy standards:** PoE-powered OT devices (controllers, sensors, access control) derive power from PoE switches that have no published redundancy standard for mission-critical or life-safety applications. If a PoE switch fails, every device it powers goes offline simultaneously — the scope of a single-point failure is the switch's entire port count. Class 4 FMP transmitters are similarly centralized, but the failure scope and recovery procedure for FMP deployments has not been standardized for OT applications either.

**Contractor training:** Electricians who install Class 4 FMP circuits are working under electrical permit and are trained through standard IBEW or NECA continuing education, which now includes Class 4 content. PoE installers are low-voltage technicians following BICSI standards — different credential, different inspection authority, different relationship to the AHJ.

---

## What the gap costs

The cost of treating these two architecturally similar technologies as completely separate domains shows up in three places.

**AHJ review time.** Every Class 4 FMP submittal that arrives at a jurisdiction where the inspector has never seen one triggers a review cycle from scratch. The inspector cannot draw on any experience with PoE power distribution, even though the fundamental architecture — centralized DC source, structured cable, remote monitoring — is the same. The inspection knowledge does not transfer because there is no framework that connects the two.

**Redundancy design quality.** Practitioners choosing between PoE and Class 4 FMP for edge OT applications are making an uninformed architectural bet. There is no published standard that tells them what N+1 PSE redundancy for PoE-powered life-safety devices looks like, and there is no published standard that tells them what UPS backup requirements for Class 4 FMP in OT applications should be. The result is that redundancy design depends on individual contractor judgment rather than an auditable standard.

**Technology adoption speed.** Both PoE and Class 4 FMP would benefit from a consolidated body of inspector familiarity, contractor training, and commissioning procedures. That body does not exist because no standards body has treated them as related technologies.

---

## What a unified framework would need to cover

A commissioning and inspection framework covering centralized low-voltage DC power distribution — regardless of whether the implementation is PoE, Class 4 FMP, or a hybrid — would need to address:

1. **Topology documentation requirements:** how the centralized source connects to the distribution cable, how loads are identified and labeled, what the fault isolation scope is for each source.

2. **Redundancy requirements by application class:** life-safety, OT/mission-critical, and convenience loads have different requirements for source redundancy and recovery time. A single standard can define these without specifying the implementation technology.

3. **Commissioning test procedures:** what functional tests must be performed after installation, and what constitutes a passing result. For both PoE and Class 4 FMP, this should include fault simulation and recovery verification.

4. **AHJ inspection checklist:** a standardized submission package that an AHJ can evaluate without deep expertise in either specific technology.

[KNOWLEDGE_GAP: No published survey of AHJ review times for Class 4 FMP permit submissions, or comparison of PoE vs. Class 4 review cycles, is available in current knowledge files. The claim that divergent standards create meaningful AHJ delay for Class 4 is supported by practitioner accounts but has not been quantified.]

---

## Who should develop it

The logical home for a unified commissioning framework is a joint working group between NFPA (which owns the NEC and has already adopted Class 4 in Article 726) and IEEE (which owns 802.3 PoE standards), with BICSI and NECA/IBEW participating on the training and inspection side.

*Synthesis: This is not a small undertaking. The two standards communities have different processes, different vocabularies, and different stakeholder bases. But the work is not technically hard — the architectural similarity between the two technologies is already well understood by practitioners. The barrier is organizational, not technical.*

The cost of inaction is concrete: every AHJ that invents a Class 4 inspection procedure from scratch is doing work that should have already been done. Every PoE-powered OT deployment that goes in without a documented redundancy standard is a future incident waiting to be attributed to the wrong root cause.

Both technologies are ready for deployment at scale. The commissioning framework that would enable that deployment at scale is not yet written.
