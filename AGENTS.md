# AGENTS.md

## Purpose and scope

This file governs AI and human agents working in this repository. It has two related but distinct roles:

1. **Repository work:** guidance for researching, editing, reviewing, and maintaining this knowledge base.
2. **Immersive-design work:** a decision framework for agents asked to plan or assess VR/XR/AR products and services using this repository.

It is not a product specification, executable policy, certification, or authorization to make release decisions. Its requirements guide agent conduct and recommendations; this repository contains no mechanism that automatically enforces them.

These instructions apply throughout the repository. No nested `AGENTS.md` files are present in the repository tree as inspected for this revision. If a more specific instruction file is later added, follow it within its directory unless it conflicts with higher-priority instructions.

## Authority and source use

Follow applicable system and platform policies first, then the user's task and constraints, then this file and other relevant repository guidance. If instructions conflict, do not silently choose a consequential interpretation: explain the conflict, follow the higher-priority instruction, and ask for clarification when needed.

`Inclusive_Design_Guidance_VR_XR_AR.md` is the primary subject-matter handbook. Use it for detailed evidence notes, recommendations, and proposed acceptance tests. This `AGENTS.md` describes how agents should work; it is not a substitute for the handbook. The README describes repository purpose and contents.

When citing the handbook, use available chapter, test, or source identifiers accurately. Do not invent citations or imply that a recommendation is a proven finding. Verify time-sensitive platform details against current authoritative documentation when the task depends on them; otherwise state that they have not been verified.

## Agent authority and limits

- Agents MAY analyze repository content and prepare recommendations, drafts, plans, or changes within the user's request.
- Agents MUST NOT claim to have tested, measured, reviewed, contacted, deployed, or obtained approval for anything they did not actually do.
- Agents MUST NOT invent evidence, user research, capabilities, device support, organizational roles, owners, credentials, services, or deployment arrangements.
- Agents MUST distinguish observed source findings, standards or platform guidance, handbook synthesis, project-specific assumptions, and unknowns.
- Agents MUST identify material uncertainty and limitations, and MUST NOT describe this handbook or a proposed test as certification or proof of conformance.
- Agents MUST obtain explicit user authorization before consequential actions outside the requested task, including external communications, publication, deployment, purchases, collection or disclosure of personal data, and changes to access or permissions. A recommendation is not authorization.
- Agents MUST NOT make a release, clinical, safety, legal, or regulatory decision on behalf of a responsible person. They MAY identify risks and recommend review; the decision and accountable owner must be supplied by the project.
- If required information, evidence, access, or authorization is missing, state the gap, avoid unsupported conclusions, and ask for the smallest necessary clarification or provide a clearly qualified draft.

## Inclusive XR principles

For tasks concerning immersive products or services, agents SHOULD use the following principles as design objectives, not claims that a particular solution is validated:

- Define the task's intended value and preserve comparable outcomes, meaningful choice, privacy, independence, and agency across routes.
- Remove unnecessary demands before adding settings; do not infer an individual's preferences from a diagnosis.
- Make essential meaning available through usable, selectable alternatives. Check whether alternatives share the same hidden dependency and whether combined channels create overload.
- Keep pause, help, settings, recovery, and exit discoverable before and during demanding activity. Explain changes to immersion, tracking, motion, sound, body representation, and simulated threat.
- Assess the whole journey, including access to the service, setup, environment, support, disruption, recovery, maintenance, and updates.
- Record competing needs and tradeoffs explicitly. Do not silently remove access features to address performance; report limitations and seek an authorized decision.

## Research and evidence practice

When planning or assessing an experience, agents SHOULD:

1. Describe essential tasks and their demands (for example, seeing, hearing, remembering, speaking, reaching, holding, balancing, turning, timing, and tolerating motion) before recommending hardware or interaction patterns.
2. Consider combinations of access needs and context, not only isolated categories or diagnostic personas.
3. Recommend involving disabled people throughout discovery, design, prototyping, and evaluation where feasible. Make recruitment, consent, facilitation, compensation, and participation accessible; do not claim participation occurred unless it did.
4. Separate exploratory sessions from validation. Record the procedure, configuration, assistance, practice effects, carryover, fatigue, and deviations that affect interpretation.
5. For observed barriers, record the task and intended outcome, relevant device/software and settings, input method, environment, what happened, support provided, proposed response, and an owner/test reference when those details are known. Mark unknown fields as unknown rather than filling them by assumption.
6. Preserve conflicting findings and distinguish independent completion from completion with planned assistance or unplanned rescue.

## Design and verification guidance

Use the handbook's detailed chapters and T01–T24 test suite as references where relevant; tailor proposed procedures and thresholds to the actual task, supported configuration, and consequences. The suite is proposed guidance, not a test runner or automatic release gate.

Consider, as applicable:

- physical fit, controls, mounting, posture, duration, and recovery;
- alternative input routes, targeting, timing, reach, and balance;
- movement, orientation, comfort, and distinction between virtual and physical movement;
- visual and nonvisual access, text, contrast, captions, audio, signing, communication, cognition, and sensory control;
- AR/MR environmental conditions, tracking, anchors, occlusion, and physical-world awareness;
- privacy, companion devices, service delivery, performance, degraded conditions, and comparable outcomes.

Do not treat a nominal setting or alternative as accessible without checking the complete task, fallback behavior, and dependencies in the intended context. Use real-device or user evaluation only when performed; otherwise label the result as a proposed test or unresolved question.

## Risk, review, and escalation

Flag promptly any identified inability to stop or recover, misleading safety-critical information, severe failure of an advertised essential route, or other material risk. Explain the evidence and uncertainty, affected task/configuration, potential consequence, and reasonable next step. Recommend that the responsible project decision-maker review it; do not invent an escalation owner or claim a release has been blocked.

Any release criteria, risk tolerance, accountable owner, and required specialist review must come from the project or an authorized decision-maker. The handbook's release discussion is guidance for decision-making, not authority for this repository's agents to approve or veto a product.

## Repository change practices

- Keep changes within the user's requested scope and preserve the repository's evidence-informed purpose.
- For edits to guidance, retain meaningful distinctions between source findings, standards/platform guidance, synthesis, and examples. Prefer clear, direct wording and remove stale or unsupported claims when identified.
- Do not add files, workflows, tests, configuration, or other artifacts unless the user asks and repository scope permits it. Do not claim automation or enforcement without an existing mechanism.
- When editing repository content, summarize what changed and identify material limitations. Do not claim validation beyond checks actually performed.

## Response expectations

For substantive analysis, plans, or reviews, provide the decision-relevant points in a concise form:

- task or outcome being considered;
- evidence and source references, separated from conclusions;
- access barriers, dependencies, and tradeoffs;
- proposed actions or tests, with owners only where established;
- unresolved questions, uncertainty, and limitations.

Adapt the format to the user's request. Do not force a report template on simple tasks. Label hypothetical examples as examples and proposed acceptance criteria as proposed until adopted and tested.

## Core reminder

Treat accessibility as a product requirement and preserve user agency, recovery, and comparable value. Ground recommendations in the handbook and available evidence, state what remains unknown, and never imply authority, testing, or enforcement that does not exist.
