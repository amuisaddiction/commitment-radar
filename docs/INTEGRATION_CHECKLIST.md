# Integration Checklist

Use this file as a live engineering checklist. Check items only after testing them.

## Omi

- [ ] Account and supported developer integration available
- [ ] Event schema confirmed from current official docs
- [ ] Webhook authentication/verification implemented where supported
- [ ] Transcript received by local backend
- [ ] Duplicate events handled idempotently
- [ ] Capture timestamp and source preserved
- [ ] Deployed webhook route tested end to end

## Qdrant

- [ ] Cloud cluster created and reachable
- [ ] Secrets configured only on backend
- [ ] Embedding model chosen and available
- [ ] Collection created with matching vector size
- [ ] Upsert tested with commitment payload
- [ ] Semantic retrieval tested with paraphrased query
- [ ] Metadata filter scopes retrieval correctly
- [ ] Persistence tested after backend restart
- [ ] Delete operation removes the relevant stored record

## Lyzr

- [ ] Current supported agent API identified
- [ ] Agent created/configured in account
- [ ] Backend authentication works
- [ ] Real API request succeeds
- [ ] Response schema validated
- [ ] Evidence is required for conflict decisions
- [ ] Error/timeout path tested
- [ ] UI logs reflect actual events, not fabricated steps

## Full workflow

- [ ] Real Omi transcript enters backend
- [ ] Commitment is extracted and validated
- [ ] Qdrant returns relevant earlier commitment
- [ ] Lyzr workflow analyzes retrieved evidence
- [ ] Conflict decision and uncertainty are shown
- [ ] Follow-up message is a draft only
- [ ] Frontend uses live API data
- [ ] Public deployed workflow passes
