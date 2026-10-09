# Demo page sources

`demo/vida-nova.html` (pt-BR, Igreja Vida Nova) and `en/demo/grace.html` (English, Grace
Community Church) are generated files. Everything needed to regenerate them is here.

| File | What it is |
|---|---|
| `gen_showcase.py` | The generator. Python 3.9+ standard library only (`zoneinfo` needs system tzdata). Its docstring documents the editorial schema. |
| `replay-BRVN26.json`, `replay-CAGR26.json` | The simulator's export of run `brca-2026-09-30`, generated on 2026-10-03: every synthetic persona's full timeline (member messages, Perto replies, morning words, weekly cards, onboarding turns), with the real Perto replies. Data, never edited. |
| `ed-BRVN26.json`, `ed-CAGR26.json` | The editorial files: which personas appear, the human-written blurbs (`role`, `chips`, `facts`, `story`, `notice`, `status`) and the whitelist of timeline events to show (`events`). This is where selection happens. |
| `faces/<stem>.jpg` | AI-generated portraits of the six personas shown, embedded in the pages as data URIs. Nobody real. |
| `qr-BRVN26.svg`, `qr-CAGR26.svg` | The WhatsApp QR codes, inlined into the pages. They encode the same `wa.me/message/…` links the editorial files carry (checked by regenerating them with segno). |
| `judge-showcase.md` | A blind judge's read of all fourteen simulated threads, with scores and the list "Bubbles that should NOT be shown". |

## Regenerate

From the repository root (paths in the editorial files are relative to it):

```sh
python3 demo/src/gen_showcase.py demo/src/replay-BRVN26.json demo/src/ed-BRVN26.json demo/vida-nova.html
python3 demo/src/gen_showcase.py demo/src/replay-CAGR26.json demo/src/ed-CAGR26.json en/demo/grace.html
```

Commit the regenerated pages together with the editorial change that produced them.

## Rules

- **Perto's words are never edited.** The pages promise "sem edição" / "unedited", so the only
  tool is selection: choose which events of a persona's timeline to show in `events`
  (a UTC `at` timestamp, optionally followed by a kind, e.g. `"2026-10-09T20:24:00 inbound"`
  when a member message and a reply share the same minute). Never change a reply's text in
  the replay or add text to a bubble.
- **The judge's do-not-show list is binding.** Nothing listed under "Bubbles that should NOT
  be shown" in `judge-showcase.md` may appear on a page, for any persona, in any selection.
- The personas are synthetic. Keep it that way: no real names, numbers or faces.
