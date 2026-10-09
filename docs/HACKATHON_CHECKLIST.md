# Hackathon Checklist

Verify the official event page for exact rules, deadline, track, and required submission fields.

## Functional proof
- [ ] Real Omi transcript reaches the deployed app.
- [ ] Qdrant Cloud stores vector records and payload metadata.
- [ ] A later transcript retrieves related history from Qdrant.
- [ ] Lyzr is genuinely invoked; show real execution/agent logs.
- [ ] Distinct agent roles are implemented/configured, not just labels in the UI.
- [ ] Conflict card includes both source snippets.
- [ ] Draft is never auto-sent.
- [ ] Forget removes data from app and configured vector memory.
- [ ] Test desktop/mobile and failure states.

## Repository
- [ ] Public GitHub repository and accepted open-source license.
- [ ] `.env` is not committed; `.env.example` has placeholders only.
- [ ] README, architecture, setup, demo URL, limitations.
- [ ] Tests pass; no API keys or private conversation data in repo.

## Deployment
- [ ] Deploy FastAPI to Render or another public host.
- [ ] Set secrets as host environment variables.
- [ ] Qdrant Cloud persistence confirmed.
- [ ] Public URL tested in incognito.
- [ ] Omi webhook points to `https://YOUR-DOMAIN/api/omi/webhook`.
- [ ] Confirm exact Omi payload shape and secret/signature mechanism.
- [ ] Manual ingest remains available as fallback.

## Submission assets
- [ ] Public demo URL and public repository URL.
- [ ] Demo video within the event's time limit.
- [ ] Title, description, track, architecture diagram.
- [ ] Explain how Omi, Qdrant, and Lyzr are each essential.
- [ ] Recheck deadline and timezone.

**Honesty rule:** configuration variables do not prove integration. A local fallback does not count as real Omi/Qdrant/Lyzr usage.
