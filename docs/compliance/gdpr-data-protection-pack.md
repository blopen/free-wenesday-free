# GDPR Data Protection Pack

This document provides a practical GDPR/DSGVO baseline for free-wenesday-free deployments. It is not legal advice. Operators must adapt it to their real processing activities, contracts, jurisdiction, and supervisory authority guidance.

## Core Principles

Use these principles for every feature that processes personal data:

- Lawfulness, fairness, and transparency.
- Purpose limitation.
- Data minimization.
- Accuracy.
- Storage limitation.
- Integrity and confidentiality.
- Accountability.

Personal data means information relating to an identified or identifiable living person. Pseudonymized data can still be personal data when re-identification is possible. Truly anonymous data must be irreversibly anonymized.

## Controller and Operator Checklist

For each deployment, document:

- Controller name and contact path.
- Data Protection Officer contact, if appointed.
- Processing purposes.
- Categories of people affected.
- Categories of personal data processed.
- Special category data, if any.
- Lawful basis for each purpose.
- Recipients and processors.
- International transfers and safeguards.
- Retention period or deletion criteria.
- Security measures.
- Data subject request workflow.
- Breach response workflow.

## Lawful Basis Mapping

Create one row per processing purpose:

| Purpose | Data | People affected | Lawful basis | Retention | Recipients | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Account access | Username, email, auth/session metadata | Registered users | Contract or legitimate interest, depending on deployment | Until account deletion plus operational/legal retention | Hosting/auth providers | Document exact provider flow |
| Collaborative AI session | Messages, prompts, generated responses, session ID | Session participants | Consent, contract, or legitimate interest, depending on deployment | Minimize; delete stale sessions | AI provider if used | Warn users before external AI processing |
| Security logs | IP, user agent, timestamps, request metadata | Visitors/users | Legitimate interest | Short operational period | Hosting/security tooling | Avoid logging secrets or message content |

## Transparency Requirements

At or before collection, provide clear information about:

- Who operates the service and how to contact them.
- Why data is processed.
- What categories of data are processed.
- Legal basis.
- Retention period.
- Recipients or processor categories.
- Transfers outside the EU, if any.
- Data subject rights.
- Complaint rights with a Data Protection Authority.
- Consent withdrawal, where consent is used.
- Automated decision-making, logic involved, and likely consequences, where applicable.

## Special Category and Sensitive Data

Do not intentionally collect sensitive data unless strictly necessary and reviewed. Sensitive categories include health data, biometric identifiers, racial or ethnic origin, political opinions, religious or philosophical beliefs, trade union membership, genetic data, sex life, and sexual orientation.

If a feature may receive sensitive content through free-text prompts or uploads:

- Warn users before submission.
- Minimize storage.
- Avoid training or analytics reuse unless explicitly reviewed.
- Apply access controls and retention limits.
- Consider a Data Protection Impact Assessment.

## DPIA Triggers

Perform a Data Protection Impact Assessment before deployment when a feature may involve:

- Systematic monitoring of people.
- Sensitive or special category data.
- Automated decision-making with significant effects.
- Large-scale profiling or evaluation.
- AI-assisted ranking, classification, moderation, recommendation, or inference about people.
- Children or vulnerable people.
- New technology with uncertain privacy impact.

## Security Baseline

- Store secrets outside the repository.
- Restrict access by least privilege.
- Encrypt transport with HTTPS.
- Protect sessions and cookies.
- Avoid logging personal data, prompts, tokens, or generated sensitive content.
- Review dependencies and remove unused packages.
- Delete temporary files and debug exports.

## Breach Basics

If personal data may be exposed:

1. Contain the incident.
2. Preserve relevant evidence.
3. Identify affected systems, data, and people.
4. Assess risk to people.
5. Notify the competent authority and affected people where legally required.
6. Document facts, effects, and remediation.

## References

European Commission GDPR guidance reviewed on 2026-07-29:

- Information duties: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/what-information-must-be-given-individuals-whose-data-collected_en
- GDPR obligations: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en
- Individual rights: https://commission.europa.eu/law/law-topic/data-protection/reform/rights-citizens/how-my-personal-data-protected/how-should-my-consent-be-requested_en
