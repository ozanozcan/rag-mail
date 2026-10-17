# rag-mail

Turns a Gmail inbox full of newsletters into a clean, tagged text corpus that RAG systems can load.

```
Gmail ─► fetch ─► save raw copy ─► move original to Trash ─► clean ─► tag by topic ─► follow free links
                                                                                        │
                                                    ~/.rag-mail/corpus/<topic>.jsonl ◄──┘
```

Status: scaffold. The pipeline is being planned.

## Your data stays yours

- All mail, corpus files and Google tokens live in `~/.rag-mail/`, outside this repo.
- Gmail access uses the `gmail.modify` scope, which can move mail to Trash but cannot delete it for good.
- `scripts/check_no_private_data.py` blocks any commit that adds a mail, corpus or credential file, or any email address outside `example.com`. It runs as a pre-commit hook (`git config core.hooksPath githooks`) and in CI next to gitleaks.
- Tests use made-up emails only.

## Scraping

Links found in emails are followed one hop, only to free pages, only where robots.txt allows it, with a rate limit. Paywalled pages are skipped.
