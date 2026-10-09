# Demo page sources

`demo/vida-nova.html` (pt-BR, Igreja Vida Nova) and `en/demo/grace.html` (English, Grace
Community Church) are generated files. Everything needed to regenerate them is here.

| File | What it is |
|---|---|
| `gen_showcase.py` | The generator. Python 3.9+ standard library only (`zoneinfo` needs system tzdata). Its docstring documents the editorial schema. |
| `replay-BRVN26.json`, `replay-CAGR26.json` | The simulator's export of run `brca-2026-09-30`, generated on 2026-10-03: every synthetic persona's full timeline (member messages, Perto replies, morning words, weekly cards, onboarding turns), with the real Perto replies. Data, never edited. |
| `ed-BRVN26.json`, `ed-CAGR26.json` | The editorial files: which personas appear, the human-written blurbs (`role`, `chips`, `facts`, `story`, `notice`, `status`), the whitelist of timeline events to show (`events`) and, where a persona is shown under another name, the declared substitution (`rename`). This is where selection happens. |
| `faces/<stem>.jpg` | AI-generated portraits of the six personas shown, embedded in the pages as data URIs. Nobody real. Present: `maria` (persona `BRVN26:p087`'s portrait, see Rules), `silvia`, `tiago` for the Portuguese page; `jun`, `kadeen`, `kwame` for the English one. |
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
  (a UTC `at` timestamp, optionally followed by a kind, e.g. `"2026-10-09T16:21:00 reply"`
  when a member message and a reply share the same minute). Never change a reply's text in
  the replay or add text to a bubble.
- **The one exception is a declared name substitution.** A persona may carry
  `"rename": {"Josefa": "Maria"}`; the generator applies that map to the persona's bubble
  texts at render time, the replay stays verbatim, and the page's lede discloses the swap. It
  is used once: the Maria card on `demo/vida-nova.html` is persona `BRVN26:p087`'s thread (the
  judge's top-ranked Brazilian thread) with "Josefa" replaced by "Maria", a more common name, by
  Rodrigo's ruling of 2026-10-09. `faces/maria.jpg` is that persona's portrait.
- **Each chat opens with the member describing what weighs on them and alternates member →
  Perto.** Never two member bubbles in a row, no thank-you chains, two or three exchanges per
  persona (Rodrigo's rulings of 2026-10-09). Day separators show the real gaps, so a reply that
  came days after the message it answers is shown with that gap, not hidden.
- **The judge's do-not-show list is binding.** Nothing listed under "Bubbles that should NOT
  be shown" in `judge-showcase.md` may appear on a page, for any persona, in any selection.
  One recorded exception, by Rodrigo's ruling of 2026-10-09: Tiago's Fri 13:21 reply
  (`2026-10-09T16:21:00 reply`) is shown. The judge excluded it for answering a three-day-old
  message and ignoring the consent remark sent that minute; the page shows the Tuesday message
  it answers, keeps the three-day gap visible in the day separators, and hides the remark.
- The personas are synthetic. Keep it that way: no real names, numbers or faces.
