# Contributing

Thank you for contributing to free-wenesday-free. Contributions are welcome when they improve the project and respect the project's privacy, security, ethics, and anti-discrimination commitments.

## Before You Start

Read:

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Privacy Policy](PRIVACY.md)
- [Ethics Policy](ETHICS.md)

By participating, you agree to follow these policies.

## Contribution Workflow

1. Fork or branch from `main`.
2. Create a focused branch with a clear name.
3. Keep commits small and reviewable.
4. Do not commit secrets, personal data, session files, generated credentials, dependency folders, or private exports.
5. Update documentation when behavior, setup, privacy, security, or user impact changes.
6. Run relevant checks before opening a pull request.
7. Open a pull request with a clear summary, validation notes, and known risks.

## Pull Request Checklist

- The change has a clear purpose.
- The diff is limited to the intended scope.
- Security and privacy impact were considered.
- User-facing behavior or configuration changes are documented.
- Relevant tests, builds, linters, or manual checks were run.
- The change does not introduce discriminatory, hateful, unsafe, or exclusionary behavior.

## Security-Sensitive Changes

Use extra care when changing:

- Authentication or authorization.
- Session handling.
- File upload, path handling, or deserialization.
- Model prompts, AI tool access, or external API calls.
- Logging, analytics, or telemetry.
- Dependency installation or build scripts.
- Storage of user data, messages, prompts, or personal information.

Security vulnerabilities should be reported privately according to [SECURITY.md](SECURITY.md).

## Privacy-Sensitive Changes

If a change collects, stores, logs, displays, exports, or sends user data to a third party, document:

- What data is processed.
- Why it is necessary.
- Where it is stored or sent.
- How long it should be retained.
- How users or operators can delete it.

## Community Standards

Be kind, direct, and constructive. Challenge ideas with evidence and respect. Do not attack people. Racism, discrimination, harassment, hate speech, and retaliation are not welcome here.
