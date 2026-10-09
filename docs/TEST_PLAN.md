# Test Plan

## Unit and API tests

Run from `backend/`:

```powershell
pytest -q
```

Initial tests cover health, manual transcript ingestion, listing, and deletion from the in-memory scaffold.

## Required functional cases

1. **New commitment:** “I'll send Rahul the invoice by Friday.” Store source text and candidate task.
2. **Genuine conflict:** “I cannot send that invoice until Monday.” Retrieve the earlier invoice promise and flag a possible deadline conflict with both evidence snippets.
3. **No conflict:** “I'll book the venue on Thursday.” Do not flag as invoice conflict without dependency evidence.
4. **Ambiguous date:** “I'll do it soon.” Do not invent an exact deadline.
5. **Unknown owner:** do not invent a person's identity.
6. **Duplicate webhook:** repeated event must not create duplicate commitments.
7. **Persistence:** stored Qdrant record remains after API restart.
8. **Deletion:** delete the relevant commitment from all supported storage layers.
9. **Provider timeout:** return a safe error and never display a fabricated success.
10. **Malformed provider output:** reject or request review instead of accepting unsupported claims.
11. **CORS:** only expected frontend origin is allowed.
12. **Secrets:** no API keys in browser bundle, logs, or public repository.

## Manual acceptance checklist

- [ ] `GET /health` succeeds
- [ ] Frontend loads at its local URL
- [ ] Manual input creates a visible item
- [ ] Error appears clearly when backend is offline
- [ ] Demo sample data is visibly labelled
- [ ] Live integration status reflects real implementation state
- [ ] Keyboard navigation and mobile layout checked
- [ ] Public deployment tested in a private/incognito browser
