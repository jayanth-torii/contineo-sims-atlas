# Contineo SIMS Atlas

**→ [jayanth-torii.github.io/contineo-sims-atlas](https://jayanth-torii.github.io/contineo-sims-atlas)**

Every function in the Contineo SIMS student ERP as it runs at Nagarjuna College of Engineering
and Technology, the login it lives in, and every operation available once you are there.

An internal requirement-capture reference, built so a rebuild team can see the whole surface
at once instead of rediscovering it login by login.

## What is in it

| | |
|---|---|
| Capabilities | **154** |
| Operations | **812** |
| Logins mapped | **7** — Department Coordinator, Faculty/Staff, HOD, SPOC, Counsellor, Student/Parent, IQAC Head |
| Login touchpoints | **232** |
| Menu entries, transcribed from screen | **114** across 13 menus |
| Overlap groups | **39** |
| Source manuals read | **19**, 387 pages |

Click any capability for its description, the path to it in each login that exposes it, the full
list of operations, the caveats, and which user manual documents it. Filter by login, category,
whether it is shared, or where the knowledge came from. Light and dark themes; the choice sticks.

## Where this came from

- Three walkthrough recordings of the live system, about four hours in total.
- Nineteen Contineo user manuals, 387 pages.
- Every menu list was read off the screen, not reconstructed from memory.

Each capability carries a **source** field — `video`, `manual`, or `both` — so you can always tell
whether something was demonstrated, merely documented, or confirmed twice.

## About the manuals

The nineteen Contineo user manuals are **not** in this repository and are not served from the site.
Eleven of them carry an explicit notice:

> This document has been prepared exclusively for the intended recipient and does not carry any
> right of reproduction or disclosure.

What they *describe* is summarised here in our own words, which is ordinary internal documentation.
The PDFs themselves stay with the college. If Contineo later gives written consent to host them,
drop the files into `manuals/` and add a link to each manual card — the manual records already
carry the exact filename.

## Still unmapped

**Admission** and **Examination**. The vendor supplied seven logins; the presenter confirmed on the
third recording that the examination login was never issued. Those two sit at either end of the
student life-cycle — everything between them is covered here.

## Rebuilding

`features.json` is the single source of truth. Both this site and the 78-page PDF atlas are
generated from it, and every total is computed, never typed.

```bash
python build/site.py          # regenerates index.html in place
```

Edit `features.json`, re-run, commit. Adding the Admission and Examination logins later means
appending capability records and a menu block — nothing else changes.

```
features.json   the dataset
index.html      the generated site (committed, so Pages can serve it)
build/site.py   the generator
```
