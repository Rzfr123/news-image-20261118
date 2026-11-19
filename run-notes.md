# Run notes — news-image-20261118

Entry title: **18 November 2026 — The World's News in One Image**

## Stories chosen (all from Wednesday 18 November 2026)

| Slot | Story | Source |
|---|---|---|
| Lead | Trump lands in Shenzhen; Xi and Putin meet a day ahead of the first US–China–Russia three-way talks | NPR, Yonhap, PBS NewsHour, Al Jazeera; Open Chronicle brief |
| Panel 1 | Iran strikes a US base in Kuwait and sites in Bahrain after US strikes on Qeshm Island | Wall Street Journal; One Turn news, 18 Nov 2026 |
| Panel 2 | Ukraine strikes the Kerch Bridge again; part of the road span collapses | Daily News brief, 18 Nov 2026; One Turn news |
| Panel 3 | Mary Peltola unseats Dan Sullivan in Alaska; Democrats take a 56–44 Senate majority | Associated Press / Alaska Public Media |
| Panel 4 | Board of Peace warns the Gaza ceasefire is at risk of collapse | Al Jazeera; Medium strategic brief, 18 Nov 2026 |
| Brief | Ebola outbreak in DR Congo passes 11,000 cases | Daily News brief, 18 Nov 2026 |
| Brief | Anthropic raises a record $81.3bn in a stock offering | One Turn news, 18 Nov 2026 |
| Brief | US loses measles-free status after 26 years | Daily News brief, 18 Nov 2026 |

Design: newspaper front page, masthead "18 NOVEMBER 2026", drawn programmatically
with `render.py` (Python + Pillow, DejaVu/Liberation fonts). No AI image generation,
so all text is exact. Simple drawn icons per story (skyline + US/CN/RU flags,
stylised Gulf map, broken bridge, Capitol dome, dove + olive branch).

## Image

- File: `entry.png`
- Dimensions: 1024 x 1024 px
- Size: 121,119 bytes (limit 1,048,576)
- SHA-256: `bd13b0d3d71b4c22f76f9826cdfac60472bae700321a02fb4ab81253fac6c0a1`

## Local tests (2026-11-19 ~11:57 WIB)

- `python3 render.py` — rendered cleanly; image visually checked three times,
  fixed headline/art overlap and two caption overflows in-session.
- `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` — exit 0,
  `out/entry.png` written, digest printed matches source.
- Ran the program twice (`out` and `out2`): both outputs byte-identical
  (sha256 `bd13b0d3...c0a1`), `cmp` clean — deterministic.
- `main.ts` also validates PNG magic bytes and the 1 MiB size limit, and
  exits non-zero on any failure. It was revised after the first test
  (added the magic/size validation + `package.json` type module).
- PIL verified `out/entry.png`: valid PNG, 1024x1024 RGB, 121,119 bytes.

## Files in repo

`main.ts`, `package.json`, `entry.png`, `render.py`, `README.md`, `LICENSE`,
`.makefun/owner.json`, `run-notes.md`, `prompt.txt`
