# Product Requirements Document (PRD)

## Problem
People make commitments in conversations but can forget them, miss deadlines, or later say something incompatible with an earlier promise.

## Target user
A freelancer, founder, or professional who wants lightweight personal accountability across conversations.

## Value proposition
“Remember what you said you'd do—and see evidence when a later statement may put it at risk.”

## MVP scope
- Receive a transcript from a supported Omi integration.
- Extract candidate task, owner, deadline, and source text.
- Store and retrieve related commitments using Qdrant.
- Use Lyzr to assess possible conflict from retrieved evidence.
- Show a reviewable alert with evidence and uncertainty.
- Draft a follow-up message for user approval.
- Provide deletion controls and transparent integration status.

## Out of scope for the hackathon MVP
- Automatically sending messages
- Full calendar/email integrations
- Enterprise team administration
- Broad personal surveillance or background recording
- Complex knowledge graphs
- Unsupported claims about perfect contradiction detection

## Success criteria
- A complete, repeatable live workflow succeeds in the deployed demo.
- Each conflict alert has traceable source evidence.
- The app distinguishes uncertain cases from clear conflicts.
- Qdrant memory persists after backend restart.
- Real provider failures are surfaced honestly.
- Public repo, architecture diagram, and demo video are complete.

## Risks
- Provider API/setup friction: validate credentials and a minimal real call early.
- False positives: require evidence and conservative labels.
- Time pressure: build a narrow vertical slice before visual polish.
- Sensitive transcripts: minimize retention and avoid logging raw content.
