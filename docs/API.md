# API reference

Interactive API docs: `/docs`

- `GET /api/health` — status and integration configuration.
- `POST /api/ingest` — JSON body: `{"transcript":"I will send the report by Friday.","source":"dashboard"}`.
- `POST /api/omi/webhook` — normalize and ingest an Omi event; adapt payload mapping to the actual event.
- `GET /api/commitments` — recent in-process records.
- `GET /api/conflicts` — recent in-process alerts.
- `GET /api/logs` — recent workflow logs.
- `POST /api/forget` — body `{"confirmation":"FORGET"}`. Current implementation clears the configured collection; change to user-scoped deletion for multi-user production.
