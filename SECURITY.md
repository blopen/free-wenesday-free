# Security Policy

## Supported Scope

Security reports are welcome for the current default branch and active project code. Experimental, archived, generated, vendored, or third-party code may have different support expectations, but maintainers still welcome responsible reports when project users could be affected.

## Reporting a Vulnerability

Please do not open a public issue for suspected vulnerabilities.

Report security concerns privately to the repository owner or maintainers through GitHub. Include enough information to reproduce and assess the issue, but do not include live secrets, personal data, or destructive exploit steps unless maintainers request a safe proof of concept.

Helpful report details:

- Affected file, endpoint, dependency, workflow, or configuration.
- Impact and likely attacker capability.
- Reproduction steps in a safe test environment.
- Whether credentials, personal data, sessions, model prompts, or API keys may be exposed.
- Suggested mitigation, if known.

## Maintainer Response

Maintainers should aim to:

- Acknowledge credible reports as soon as practical.
- Triage severity and affected versions.
- Keep sensitive details private until a fix or mitigation is available.
- Credit reporters when appropriate and requested.
- Publish security notes when users need to take action.

## Secure Development Baseline

- Do not commit secrets, API keys, tokens, passwords, private certificates, session stores, or personal data.
- Keep dependencies updated and remove unused dependencies where possible.
- Validate and sanitize untrusted input.
- Use least-privilege access for services, tokens, and integrations.
- Store secrets in environment variables or a secret manager, not in source control.
- Protect authentication, authorization, and session handling with extra review.
- Review AI-assisted features for prompt injection, data leakage, unsafe tool use, and unintended disclosure.
- Avoid logging sensitive content, credentials, personal data, or private model conversations.

## Disclosure Principles

Coordinated disclosure protects users. Public disclosure should wait until maintainers have had a reasonable opportunity to investigate and mitigate the issue, unless there is an urgent public safety reason.
