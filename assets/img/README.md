# assets/img

Screenshots of the pastor's dashboard: a Portuguese set (`painel-*`) used on `igrejas.html` and an English set (`dashboard-*`) used on `en/churches.html`.

## Portuguese set (`painel-*`)

- Source: the **perto-sim** deployment's dashboard (Igreja Vida Nova, BRVN26), Simulation view, light theme, product commit `1f0c0a5` on `develop`, captured 2026-10-08 (evening, ET).
- Every row is a simulated persona. The strip "Simulação — dados sintéticos. Nenhuma pessoa real." and the ⚗️ badges are kept in frame on purpose and must never be cropped out (see the product's `docs/PHASE-2-SIMULATION-DESIGN.md` §3.4).
- Capture: viewport slices at 1327 CSS px wide (1x), stitched into one page image and cropped at the bottom; the care queue shows the "Em andamento" filter. WebP (quality 88) is served first, PNG is the fallback.
- To regenerate: open the sim dashboard from the sim console ("Open Sim dashboard"), pick "Tema claro", visit `#/pulse`, `#/guides`, `#/care`, capture, and keep the same file names and widths (1328 px).

## English set (`dashboard-*`)

- Source: the **perto-sim** deployment's dashboard (Grace Community Church, CAGR26, locale `en`), Simulation view, light theme, product commit `21f4c75` on `develop`, captured 2026-10-09 (morning, ET).
- Every row is a simulated persona. The strip "Simulation — synthetic data. No real people." and the ⚗️ badges are kept in frame on purpose and must never be cropped out.
- Capture: the same method as the Portuguese set. Viewport slices at 1326 CSS px wide, the widest this laptop's screen allowed (the display reported `devicePixelRatio` 1.09, but the slices came out at CSS-pixel size, 1326 px for a 1326 px viewport, so one image pixel is one CSS pixel), stitched into one page image and cropped at the bottom, then one pixel of each edge replicated so the files keep the 1328 px width. The care queue shows the default "All (3)" filter: CAGR26 has no new or in-progress requests, so its three requests are all "Closed this week". WebP (quality 88) is served first, PNG is the fallback.
- Sizes: `dashboard-pulse` 1328×1210, `dashboard-sermon-group` 1328×1327, `dashboard-care-queue` 1328×884.
- To regenerate: open the sim dashboard from the sim console for CAGR26 ("Open Sim dashboard"), pick "Light theme", visit `#/pulse`, `#/guides`, `#/care`, capture, and keep the same file names and widths (1328 px).
