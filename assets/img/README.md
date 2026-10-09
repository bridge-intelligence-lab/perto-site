# assets/img

Three screenshots of the pastor's dashboard, used on `igrejas.html` and `en/churches.html`.

- Source: the **perto-sim** deployment's dashboard (Igreja Vida Nova, BRVN26), Simulation view, light theme, product commit `1f0c0a5` on `develop`, captured 2026-10-08 (evening, ET).
- Every row is a simulated persona. The strip "Simulação — dados sintéticos. Nenhuma pessoa real." and the ⚗️ badges are kept in frame on purpose and must never be cropped out (see the product's `docs/PHASE-2-SIMULATION-DESIGN.md` §3.4).
- Capture: viewport slices at 1327 CSS px wide (1x), stitched into one page image and cropped at the bottom; the care queue shows the "Em andamento" filter. WebP (quality 88) is served first, PNG is the fallback.
- To regenerate: open the sim dashboard from the sim console ("Open Sim dashboard"), pick "Tema claro", visit `#/pulse`, `#/guides`, `#/care`, capture, and keep the same file names and widths (1328 px).
