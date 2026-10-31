# perto.life

Static site for Perto: front page, privacy policy, the churches page and two demo pages (`demo/`, `en/demo/`), in pt-BR (root) and English (`/en/`). No build step, no framework, no cookies. Served by GitHub Pages.

Visits are counted with [GoatCounter](https://www.goatcounter.com/), cookieless: `count.js` in every `<head>` sends one beacon per page view, the WhatsApp buttons send one event each (`event/whatsapp/<source>`, see `assets/site.js`) and the QR codes land on `go/` first so a scan is counted (`event/qr/<church>`) before the redirect to `wa.me`. No cookies, nothing stored in the browser except the theme choice (`localStorage` key `perto-theme`) and, once a visitor clicks "English" or "Português" in the nav, that language choice (`perto-lang`).

The two front pages (`/` and `/en/`) open in the visitor's language: an inline script in each `<head>` sends a phone whose first language is Portuguese to `/` and any other to `/en/`, before anything paints. A remembered nav choice wins over the phone's language, and nothing redirects when the visitor comes from another page of the site. Every other page stays exactly where its link points, so a shared demo or churches link always opens what was sent.

## Files

| Path | What |
|---|---|
| `index.html`, `en/index.html` | Front page |
| `privacidade.html`, `en/privacy.html` | Privacy policy — also the URL Meta needs for the WhatsApp app |
| `igrejas.html`, `en/churches.html` | Design-partner / interest page, with the dashboard screenshots |
| `assets/site.css` | The one stylesheet (tokens, both themes, phone first) |
| `assets/site.js` | The one script: the theme toggle, the remembered language choice and the WhatsApp click counts |
| `assets/img/faces/` | The six demo portraits (AI-generated, nobody real) at 168 px, for the demo cards on the churches pages |
| `demo/`, `en/demo/` | The demo pages, generated from `demo/src/` (see its README) |
| `go/` | `vida-nova.html` and `grace.html`: what the QR codes encode (`https://perto.life/go/vida-nova`, `/go/grace`). Each counts the scan and redirects to the church's `wa.me` link; `noindex` |
| `assets/img/` | Dashboard screenshots on synthetic data (see its README) |
| `CNAME` | `perto.life` for GitHub Pages |

## Before publishing (Rodrigo)

1. Remove the yellow draft bar from each page (`<div class="draft">…</div>` and the comment above it).
2. Fill the `to confirm` items on both privacy pages: effective date, the controller's postal address.
3. Create (or forward) the two mailboxes: `privacidade@bridgeintelligence.ca` (privacy officer / DPO) and `igrejas@bridgeintelligence.ca` (church interest). Or change the addresses.
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
