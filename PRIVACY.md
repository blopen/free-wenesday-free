# Privacy Policy

## Purpose

This document sets the privacy baseline for free-wenesday-free. It is written as a project policy, not as individualized legal advice. Deployers and operators are responsible for checking their own legal obligations, including DSGVO/GDPR requirements where applicable.

## Privacy Principles

- Collect only the data needed for a clear project purpose.
- Prefer anonymous, local, or aggregated data where possible.
- Do not collect sensitive personal data unless there is a documented need and a lawful basis.
- Do not commit personal data, user exports, logs, session files, credentials, or API keys to the repository.
- Make data flows visible in documentation when features process user content.
- Delete data that is no longer needed.
- Protect data with appropriate technical and organizational measures.

## Personal Data

Depending on deployment, the application may process:

- Account data such as usernames or email addresses.
- User-generated content, messages, prompts, algorithm descriptions, or uploaded files.
- Technical data such as IP addresses, device information, logs, cookies, sessions, or error traces.
- API usage data from external services used by an operator.

Operators should document which data is actually collected in their deployment, why it is needed, how long it is retained, and who can access it.

## DSGVO/GDPR-Oriented Rights

Where DSGVO/GDPR applies, users may have rights to:

- Access their personal data.
- Correct inaccurate data.
- Request deletion.
- Restrict or object to processing.
- Receive portable copies of data where applicable.
- Withdraw consent where consent is the lawful basis.

Project operators should provide a clear contact path for privacy requests and verify requester identity before disclosing or deleting data.

## AI and Third-Party Processing

Some features may use external AI, hosting, analytics, authentication, database, or infrastructure providers. Operators must review provider terms, data processing agreements, retention settings, regional storage, and opt-out controls before sending personal data to third parties.

Do not send secrets, confidential information, or unnecessary personal data to model providers or third-party APIs.

## Cookies, Sessions, and Logs

Use cookies and sessions only where necessary for security, authentication, preferences, or core functionality. Logs should be limited, access-controlled, and scrubbed of sensitive data where possible.

## Data Retention

Retain personal data only for as long as needed for the documented purpose, legal obligations, security investigation, or user-requested functionality. Delete temporary files, generated exports, debug logs, and test data when no longer required.

## Breach Handling

If personal data may have been exposed, maintainers and operators should investigate quickly, preserve relevant evidence, mitigate the issue, and follow applicable notification obligations.
