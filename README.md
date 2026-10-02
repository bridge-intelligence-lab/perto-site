# perto.life

Static site for Perto: front page, privacy policy and the churches page, in pt-BR (root) and English (`/en/`). No build step, no framework, no cookies. Served by GitHub Pages.

## Files

| Path | What |
|---|---|
| `index.html`, `en/index.html` | Front page |
| `privacidade.html`, `en/privacy.html` | Privacy policy — also the URL Meta needs for the WhatsApp app |
| `igrejas.html`, `en/churches.html` | Design-partner / interest page |
| `assets/site.css` | The one stylesheet (tokens, both themes, phone first) |
| `CNAME` | `perto.life` for GitHub Pages |

## Before publishing (Rodrigo)

1. Remove the yellow draft bar from each page (`<div class="draft">…</div>` and the comment above it).
2. Fill the `to confirm` items on both privacy pages: effective date, the controller's postal address.
3. Create (or forward) the two mailboxes: `privacidade@perto.life` (privacy officer / DPO) and `igrejas@perto.life` (church interest). Or change the addresses.
4. Optional: paste a form embed (Tally works on a static site) into the `form-box` on both churches pages, replacing the mailto fallback.

## Publishing on GitHub Pages

1. Create the repo `bridge-intelligence-lab/perto-site` (public — Pages on a private repo needs a paid plan), push this folder's `main`.
2. Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`. Custom domain: `perto.life`. Tick *Enforce HTTPS* once the certificate is issued (minutes to an hour).
3. At the registrar, point the apex and `www`:

   ```
   A     @    185.199.108.153
   A     @    185.199.109.153
   A     @    185.199.110.153
   A     @    185.199.111.153
   CNAME www  bridge-intelligence-lab.github.io
   ```

4. Check: `curl -sI https://perto.life/privacidade.html | head -1` → `HTTP/2 200`.

## After it is live

- Meta App Dashboard → Settings → Basic → Privacy Policy URL: `https://perto.life/privacidade.html` (and the data-deletion instructions URL: the same page, section 7).
- WhatsApp business profiles: set `websites` to `https://perto.life` on both numbers (one Graph call each).
- Business Verification can cite the domain.
