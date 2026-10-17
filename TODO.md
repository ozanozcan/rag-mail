# TODO

Parked 2026-10-17. Pick up with `/mow plan rag-mail`.

- [ ] Plan the pipeline (`/mow plan rag-mail`): fetch → save → trash → clean → tag → scrape.
- [ ] Google Cloud setup (owner, ~10 min): project, Gmail API on, OAuth desktop client, `client_secret.json` in `~/.rag-mail/`.
- [ ] Fetch: Gmail API, `gmail.modify` scope; save raw `.eml` to `~/.rag-mail/raw/`, read it back, then move the message to Trash.
- [ ] Clean: strip HTML, footers, tracking links; drop duplicates.
- [ ] Tag by topic: football, fitness, coding, career, mind, junk. Score tagging against a hand-labelled sample.
- [ ] Scrape: one hop from links in the mail, free pages only, robots.txt + rate limit, skip paywalls.
- [ ] Write `~/.rag-mail/corpus/<topic>.jsonl`; measure how much is content vs sales copy.
- [ ] Hand-off: football → HLC, fitness → FitnessManager RAG, coding/career/mind → docrag.
- [ ] Prove the guard in CI too: push a branch with a fake leak, confirm the `guard` check fails.
