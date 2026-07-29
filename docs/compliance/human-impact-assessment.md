# Human Impact Assessment

Use this assessment before merging or deploying features that affect real people, process personal data, use AI, or influence access, visibility, safety, wellbeing, opportunity, moderation, ranking, or decisions.

## Feature Summary

- Feature name:
- Owner:
- Review date:
- Intended purpose:
- People affected:
- Deployment context:
- AI or automated components:
- Personal data involved:

## Real People Review

Answer in plain language:

- Who can benefit from this feature?
- Who can be harmed, excluded, misclassified, surveilled, or pressured?
- Could this feature affect a person's rights, dignity, reputation, access, safety, work, education, money, health, or housing?
- Could children, vulnerable people, marginalized groups, or people in crisis be affected?
- Could the feature amplify racism, discrimination, harassment, or hate?

## Privacy Review

- What personal data is collected or inferred?
- Is every data field necessary?
- What is the lawful basis in the deployment context?
- How long is data retained?
- Can a person access, correct, delete, restrict, or export their data?
- Are prompts, outputs, logs, embeddings, or analytics treated as personal data where linked to a person?

## Fairness and Anti-Discrimination Review

- Could outputs differ unfairly by language, race, ethnicity, religion, gender, disability, age, sexuality, class, nationality, or other protected traits?
- Are there feedback or appeal paths for harmful results?
- Is human review available before sensitive action is taken?
- Are moderation and enforcement rules applied consistently?

## AI Safety Review

- Is AI involvement visible to users?
- What model/system is used?
- Can users overtrust the output?
- Can prompt injection or unsafe tool use expose data or trigger harmful actions?
- Are there limits on high-impact decisions?
- Are logs monitored for failures without collecting excessive personal data?

## Accessibility Review

- Can people use the feature with assistive technologies?
- Is the language clear and respectful?
- Are there alternatives for people who cannot or do not want to use AI features?
- Does the feature avoid unnecessary friction for people with disabilities or limited technical experience?

## Decision

Choose one:

- Approved.
- Approved with mitigations.
- Blocked pending privacy review.
- Blocked pending security review.
- Blocked pending ethics review.
- Blocked pending legal review.

## Required Mitigations

| Risk | Mitigation | Owner | Due date | Status |
| --- | --- | --- | --- | --- |
| | | | | |

## Reviewer Notes

Record assumptions, evidence, and unresolved questions. Keep this document with the pull request or release notes when the feature affects people materially.
