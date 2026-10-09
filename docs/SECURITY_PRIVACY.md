# Security & Privacy

- Never commit `.env`, API keys, webhook secrets, or private transcripts.
- Use synthetic demo data in screenshots and demo recordings.
- This scaffold's Forget endpoint has confirmation but no user authentication; do not expose as multi-user production without authentication and ownership checks.
- In-process timeline/conflict lists reset on restart and are not multi-user safe.
- Use the actual webhook-signature mechanism supported by Omi, if available.
- Add user authentication, authorization, rate limits, retention settings, and per-user Qdrant isolation before storing real conversations.
- Drafts are not sent automatically.
- Conflict alerts can be false positives or missed conflicts; always show evidence.
