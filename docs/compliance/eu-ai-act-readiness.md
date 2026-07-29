# EU AI Act Readiness Pack

This document helps free-wenesday-free contributors and operators prepare AI features for the EU AI Act. It is a project readiness checklist, not legal advice.

## Timeline Snapshot

Based on European Commission guidance reviewed on 2026-07-29:

- The AI Act entered into force on 2024-08-01.
- Prohibited AI practices and AI literacy obligations apply from 2025-02-02.
- Governance rules and obligations for general-purpose AI models apply from 2025-08-02.
- The AI Act becomes generally applicable on 2026-08-02, with exceptions.
- Certain high-risk rules are subject to later transition timelines, including 2027-12-02 for some high-risk use cases and 2028-08-02 for high-risk AI embedded in regulated products, according to Commission implementation guidance available on 2026-07-29.

Always verify current legal status before deployment.

## Role Mapping

For every AI feature, document whether the project/operator acts as:

- Provider: develops or places an AI system/model on the market or puts it into service under its own name.
- Deployer: uses an AI system under its authority.
- Importer or distributor: makes another provider's AI system available in the EU.
- Product manufacturer: embeds AI in a regulated product.
- General-purpose AI model provider or downstream integrator.

## AI Inventory Template

| Feature | Purpose | AI model/system | Role | People affected | Data used | Risk category | Human oversight | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Collaborative chat | Assist users in shared sessions | External or configured LLM | Deployer or provider, depending on deployment | Session participants | Prompts, messages, outputs | Triage required | User/operator review | Draft |

## Prohibited Practice Triage

Do not build, deploy, or assist features that enable:

- Manipulative or deceptive techniques that materially distort behavior and cause or are likely to cause significant harm.
- Exploitation of vulnerabilities based on age, disability, or social/economic situation causing or likely to cause significant harm.
- Social scoring leading to detrimental or unfavorable treatment.
- Certain biometric categorization, emotion recognition, predictive policing, or untargeted scraping use cases prohibited by the AI Act.

Escalate any feature near these categories before implementation.

## High-Risk Triage

Escalate for legal and maintainer review when AI is used for or materially affects:

- Education or vocational training access, scoring, or evaluation.
- Employment, worker management, hiring, promotion, termination, or task allocation.
- Access to essential private or public services.
- Creditworthiness, insurance, housing, healthcare, benefits, or similar access decisions.
- Law enforcement, migration, asylum, border control, or justice contexts.
- Biometric identification or categorization.
- Safety components in regulated products.

High-risk systems may require risk management, data governance, technical documentation, logging, transparency, human oversight, robustness, accuracy, cybersecurity, conformity assessment, registration, and post-market monitoring.

## AI Literacy

Maintainers and deployers should make sure people configuring, reviewing, or operating AI features understand:

- The intended purpose and limitations.
- Data protection and confidentiality rules.
- Prompt injection and unsafe tool-use risks.
- Bias, discrimination, hallucination, and overreliance risks.
- When human review is required.

## Transparency and Human Oversight

AI-facing user experiences should make clear when AI is involved, what it can and cannot do, and how people can challenge or correct harmful output. Human oversight must be meaningful for sensitive workflows.

## Documentation Checklist

Before merging AI-impacting changes, document:

- Intended purpose.
- Model/system used.
- Role mapping.
- People affected.
- Data categories.
- Risk triage result.
- Human oversight path.
- Logging and retention choices.
- Known limitations.
- Monitoring and incident response.

## References

European Commission guidance reviewed on 2026-07-29:

- AI Act overview and timeline: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- Navigating the AI Act FAQ: https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act
