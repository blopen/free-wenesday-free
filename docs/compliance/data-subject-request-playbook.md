# Data Subject Request Playbook

This playbook helps maintainers and operators respond to GDPR/DSGVO rights requests from real people. It is not legal advice. Adapt deadlines, identity checks, and exceptions to the actual deployment and applicable law.

## Supported Request Types

People may request:

- Information about processing.
- Access to their personal data.
- Correction of inaccurate or incomplete data.
- Erasure when data is no longer needed or processing is unlawful.
- Restriction of processing.
- Data portability where applicable.
- Objection to processing.
- Withdrawal of consent where consent is used.
- Human review or information about automated decision-making where applicable.

## Response Time

Respond without undue delay and generally within 1 month of receiving a valid request. If the request is complex or numerous requests are made, document any legally available extension and inform the person in time.

## Intake Template

Record:

- Date received.
- Requester contact.
- Request type.
- Relevant account, session, identifier, or context.
- Identity verification status.
- Systems to search.
- Data found.
- Action taken.
- Response date.
- Reviewer.
- Exceptions or refusal reason, if any.

## Workflow

1. Acknowledge receipt where practical.
2. Classify the request type.
3. Verify identity using proportionate information.
4. Locate relevant systems and processors.
5. Export, correct, delete, restrict, or explain as appropriate.
6. Review for third-party data, security secrets, legal holds, or abuse risk.
7. Respond in clear language.
8. Log the outcome without storing unnecessary personal data.

## Erasure Checklist

Before deleting, check whether data must be kept for:

- Legal obligations.
- Security investigation.
- Establishment, exercise, or defense of legal claims.
- Freedom of expression or public interest exceptions.
- Irreversibly anonymized statistical or research purposes where applicable.

If deletion is appropriate:

- Delete primary records.
- Delete stale sessions and temporary files.
- Ask processors to delete where required.
- Remove search indexes or derived records where feasible.
- Preserve only minimal audit proof of completion.

## AI-Specific Request Handling

When AI features are involved, check:

- Prompts and messages.
- Generated outputs linked to the person.
- Conversation history.
- Embeddings, vectors, indexes, or summaries.
- Moderation or classification labels.
- Tool-call logs.
- Third-party AI provider retention settings.

Do not promise deletion from third-party model training unless the operator has verified the provider terms and controls.

## Refusal or Limitation

If a request is refused or limited, explain the reason, the right to complain to a Data Protection Authority, and available judicial remedies where required.

## Reference

European Commission request-handling guidance reviewed on 2026-07-29: https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/dealing-individuals-requests_en
