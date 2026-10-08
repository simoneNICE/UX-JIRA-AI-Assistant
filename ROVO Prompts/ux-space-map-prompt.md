# Rovo Chat prompt — Cross-project space map (manager)

Shows where a designer works and where the demand comes from: which
Jira projects hold their assigned items, and which projects hold
the parents and grandparents of those items. One person at a time.
Paste into Rovo Chat.

---

You are helping me see which Jira projects a single UX designer touches — where their assigned work lives and where the parent chain of that work lives. Read-only — do not create, edit, or transition any issues.

INPUT — ask me first. Before running any query, ask me exactly this and wait for my answer:
"Which designer do you want the space map for? (give me a name)"
Resolve the name from the rosters below. If the name isn't in the rosters or is ambiguous, tell me and ask again.

ROSTER — Israel designers (account_id in parentheses):
Yaara Bar (557058:f02910b4-7a33-4532-ae52-65b2d02fc245), Chelsea Franz (712020:65c25382-da24-4a4f-9c1a-b9794892207f), Assaf Zinger (712020:0861d082-a1db-4b17-aeba-563afe001639), Eitan Koren (712020:5e21d1f2-366c-4c8e-90fe-3bfb9247687d), Tali Silon-Shacham (70121:f9675544-965d-4261-8c69-dd0b5af1f36b), Erez Bar (63ea3e479e626e54cc5ab8fd), Michael Dalal (712020:e6a03127-1281-4a20-a573-1cc6d59fcf0d), Yoav Chen (61151844627b5600688e908b), Libi Becker Tidhar (61190114650a26006e0f1823), Sveta Fomchenko (712020:d95bc91f-6277-4ae6-988a-bf4a191b66be), Lee Winkler (62cd77d61e326fd9301283b1), Lihi Shrem (712020:b7ff7587-41a6-4539-ba06-e2da1ca0810c), Tal Segev (712020:826cc4e2-1cd8-4e8e-ac09-c37294c8d27e).

ROSTER — India designers (account_id in parentheses):
Advait Patil (712020:7514f68a-9d45-45f5-8c66-991834165754), Ajit Vaidya (63adc588741248746bf6bdcc), Deepa Bhamare (62b16a22cebad33432f6b5c6), Deepak Badgujar (622ba91e8a4bb60068f70032), Dinesh Koli (712020:721636e8-4f81-48c0-aa3e-d38298047b60), Gajanan Rajput (712020:aa37b218-7608-4133-9500-aac224528ebc), Manashree Thokal (712020:ddc645bb-ccd2-41f5-9cc4-c019304c84e0), Mayur Chaudhari (712020:d488a8df-551b-4325-aa41-7d8e1dababca), Parimal Khanolkar (712020:27f92cd9-b054-4cf2-9ef0-56b974e21536), Prafull Mane (62cdb715dcf59ca4ad0145d2), Sheetal Barge-Gole (712020:c7abe286-b08a-4898-a5c1-9276f430c8df), Shikha Shukla (62baf1fbd752af0e54ebfa75), Sushanth Civi (712020:df95749d-30dc-4c39-b333-aa73a4742b7a), Tapas Chowdhury (626094579506d6006fd9fec6), Umajit Mongjam (70121:d43b183a-1a5a-41a1-87ec-cc0e549e8adc), Kalpesh Gurav (712020:8dab633f-0bed-41cd-b93a-d7d95746b0b5), Nirmitee Sisodia (712020:2f630343-f304-4df5-bcb2-ea638aaa72b5).

ROSTER — USA designers (account_id in parentheses):
Doug Clement (6077f6ccb5dffc006f4cb020), Janet Gonzales (6307037507b7804d7aa1da43), David Stoker (712020:ba6ab7d2-69f7-44ae-b2dc-e534b51c426e), Sara Evans (712020:8e26db37-d04f-4937-b9fd-0b5779f0485a), Lorina Binning (611cf7d5ee947000719686d9), Serena Yang (6318920b6856bdd60aa03d2b), Andrew Wong (712020:ce3e4425-40fd-4dee-bceb-7a773f98b5b9).

FIELD NOTES:
- Only status New or In Progress. Exclude Done and Removed entirely.
- Issue types in scope: Task, Story, Epic. Sub-tasks excluded.
- Do NOT restrict to project = CXUX — designers may have items in any project.
- A project key is the prefix of an issue key (e.g. CXUX-12345 → project CXUX). Use this to derive a parent's or grandparent's project from its key without extra lookups.

STEPS — work one person at a time:

1. Find all issues assigned to this person where type is Task, Story, or Epic and status is New or In Progress. No project filter. For each, record the issue key, type, and parent key (if any).

2. Collect the distinct parent keys from step 1. In one batch query (`issue in (KEY1, KEY2, …)`), fetch those parents and record each one's parent key (the grandparent). Do NOT query parents one by one.

3. Build three project lists by extracting the project prefix from each key:
   a. **Works in** — distinct projects from the person's own assigned items (step 1).
   b. **Parent projects** — distinct projects from the parent keys (step 1). Flag any that differ from the "Works in" list.
   c. **Grandparent projects** — distinct projects from the grandparent keys (step 2). Flag any that differ from the "Works in" list.

4. Output — keep it short, split by status:

```
# Space map — <Name>
*<date>*

## New
Works in: CXUX (5), CXREC (1)
Parents in: CXUX (3), **CXREC** (2)
Grandparents in: **CXREC** (2), CXUX (1)

## In Progress
Works in: CXUX (9)
Parents in: CXUX (5), **PMN** (2)
Grandparents in: **CXREC** (2), CXUX (3), **PMN** (1)
```

Bold a project name when it does NOT appear in the "Works in" list — that is true cross-project demand.
If a status section has zero items, show "None" on one line.
If the person has zero active items overall, just say so.

Read-only — do not create, edit, or transition any issues.
