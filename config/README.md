# Career OS source configuration

These files are plain-text configuration intended for manual editing. Users do not need to modify application code to maintain the source lists.

## Files and record formats

- platforms.txt: Platform Name | Base URL | Adapter ID | Enabled
- companyportals.txt: Company Name | Official Careers URL | Market | Category | Enabled
- recruitment_sources.txt: Consultancy Name | Official Website URL | Geography | Specialization | Enabled

## Editing

1. Open the file in Notepad, VS Code or another plain-text editor.
2. Add one record per line, following the exact field order above and in the file header.
3. Keep the pipe character as the field separator.
4. Save as UTF-8 plain text.
5. Commit and push the change to the intended branch.
6. Refresh or restart Career OS source configuration.

Lines beginning with # are comments. Blank lines are ignored. Do not put a pipe character inside a field.

## Source registration is not scraper support

Adding a URL only registers a candidate source. Career OS must validate the URL, check source terms and access restrictions, map it to a registered adapter, and run a health check. Unsupported sources must be reported visibly, never silently skipped.

Expected states: supported, pending, disabled, temporarily_unavailable, blocked_or_restricted.

## User-specific configuration

Repository files are shared starter defaults. Self-hosted users must be able to maintain local overrides. Public-edition users must have account-scoped overrides. One user's changes must not affect another user's source list. When upstream defaults change, show a merge/diff rather than overwriting local edits.

## Security and compliance

Never store API keys, cookies, passwords, tokens, private recruiter contacts or candidate personal data in these files. Respect site terms, rate limits, authentication boundaries, anti-bot controls, privacy and anti-spam requirements.
