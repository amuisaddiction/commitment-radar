# UI/UX Design

## Product
**Commitment Radar** — a calm, trustworthy assistant that remembers spoken commitments and flags possible conflicts with supporting evidence.

## Design system
- Canvas `#101522`, sidebar `#0C111D`, surface `#171E2D`, borders `#293247`
- Primary text `#F3F5FB`, muted `#8F9BB1`
- Primary action `#88ADFF`, warning `#FFC46B`, success `#76E0B3`, accent `#B8A0FF`
- DM Sans body; Manrope headings
- Desktop sidebar + responsive dashboard cards; single-column layout on mobile.

## Screens/sections
1. Overview metrics: open commitments, possible conflicts, memory status, Lyzr status.
2. Quick Capture: transcript input, Analyze action, visible result.
3. Agent Workflow: extract, retrieve, conflict-check, draft stages.
4. Conflict Radar: severity, explanation, two quoted evidence snippets, suggested message.
5. Recent Commitments: task, source, recipient, deadline, confidence.
6. Agent Activity: execution statuses and messages.
7. Privacy: explicit Forget memory action with confirmation.

## UX principles
- Say “possible conflict,” not “you broke a promise.”
- Show evidence before recommendations.
- Never auto-send drafted messages.
- Clearly label demo fallback vs real integrations.
- Keep the manual transcript fallback available if Omi webhook fails.
- Test empty, success, conflict, error, mobile, and Forget states.
