# assets/img

Screenshots of the pastor's dashboard: a Portuguese set (`painel-*`) used on `igrejas.html` and an English set (`dashboard-*`) used on `en/churches.html`.

## Portuguese set (`painel-*`)

- Source: the **perto-sim** deployment's dashboard (Igreja Vida Nova, BRVN26), Simulation view, light theme, product commit `1f0c0a5` on `develop`, captured 2026-10-08 (evening, ET).
- Every row is a simulated persona. The strip "Simulação — dados sintéticos. Nenhuma pessoa real." and the ⚗️ badges are kept in frame on purpose and must never be cropped out (see the product's `docs/PHASE-2-SIMULATION-DESIGN.md` §3.4).
- Capture: viewport slices at 1327 CSS px wide (1x), stitched into one page image and cropped at the bottom; the care queue shows the "Em andamento" filter. WebP (quality 88) is served first, PNG is the fallback.
- To regenerate: open the sim dashboard from the sim console ("Open Sim dashboard"), pick "Tema claro", visit `#/pulse`, `#/guides`, `#/care`, capture, and keep the same file names and widths (1328 px).

## English set (`dashboard-*`)

- `dashboard-pulse` and `dashboard-care-queue`: the **perto-qa** deployment's dashboard, Grace Community Church (CAGR26, locale `en`) demo congregation, Simulation view (seeded synthetic data), light theme, product commit `21f4c75` on `develop`, captured 2026-10-09 (morning, ET). On this deployment the Simulation view marks itself with the "Live | Simulation" view toggle ("Simulation" selected) and the ⚗️ badges, one beside the toggle, one beside each page title and one on every care-queue row, rather than the sim deployment's strip sentence; the toggle and the badges are kept in frame on purpose and must never be cropped out.
- `dashboard-sermon-group`: the **perto-sim** deployment's dashboard, Grace Community Church (CAGR26), Simulation view, light theme, locale `en`, product commit `21f4c75` on `develop`, captured 2026-10-09 (morning, ET), with the sim's strip sentence "Simulation — synthetic data. No real people." and the ⚗️ badges in frame. Why the sim for this one: QA's seeded demo guide carries no verified passage text, so its screen prints "reference not verified — text not shown".
- Every row is a synthetic persona on both deployments.
- Capture: the same method as the Portuguese set. Viewport slices at 1326 CSS px wide, the widest this laptop's screen allowed (the display reported `devicePixelRatio` 1.09, but the slices came out at CSS-pixel size, 1326 px for a 1326 px viewport, so one image pixel is one CSS pixel), stitched into one page image and cropped at the bottom, then one pixel of each edge replicated so the files keep the 1328 px width. WebP (quality 88) is served first, PNG is the fallback.
- `dashboard-pulse` (1328×507) is cropped just below the "What your congregation is praying about" card on purpose: the gratitude and suggestion cards and the chart stay out until the suggestions are localized (product story filed 2026-10-09) and the next Monday pulse has run, when it is to be retaken in full. `dashboard-sermon-group` (1328×1327) ends at the guide card's bottom edge, after its two buttons. `dashboard-care-queue` (1328×1120) shows the default "All (4)" filter, one new, two in progress and one closed request, and ends after the monthly-report line.
- To regenerate: open CAGR26's dashboard from the QA console with the Simulation view (from the sim console for the sermon image), pick "Light theme", visit `#/pulse`, `#/guides`, `#/care`, capture, and keep the same file names and widths (1328 px).
