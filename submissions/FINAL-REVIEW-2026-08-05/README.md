# Final Visual Review — 2026-08-05

All four packages. Every PDF page 1 displays
`HONEST-STATE REVIEW DRAFT — NOT SUBMISSION CANDIDATE`.

**Last refreshed: 2026-08-08 (UltraQA verify + QA hash resync)**

| File | SHA256 |
|---|---|
| FrameA-eswa-honest-review.pdf | `285b5584cbd1ffeb23f76f51e771113ebae2c89e383e4fc9e9568d92c1d23074` |
| D2-neurocomputing-honest-review.pdf | `8e1624c31e04565f6b9e63a299503e1a4fb1790d0cb0cbae4336262bd2b12a65` |
| B6-ieee-tetci-honest-review.pdf | `e3969144a83cc824e28d79469ed5beb7173a76cef56e4c698663641c5e299faf` |
| PaperB-neurocomputing-honest-review.pdf | `bd6c7ff094aefe9bae272f2bf97f230c8195450aa5f4de3f32b701cc79a72944` |

Second-round fixes (verified):
- **Frame-A**: All 10 tikz figures scaled to textwidth (x=0.83081pt); overfull=0; GPU unit aligned (GPU-s throughout); figures-qa refreshed (08-05)
- **PaperB**: fig03 x-axis labels now two-line short form (cross/probe, within/probe, edit/level), angle=0, no overlap; 0 overfull
- **FINAL-REVIEW PDFs**: replaced with post-repair versions; contact sheets regenerated
- **D2 figures-qa page-001**: refreshed (was stale blank raster)

Third-round fixes (2026-08-06, verified):
- **PaperB**: banner merged into the title block so page 1 carries banner+title+abstract
  (no blank cover page); fig03 rebuilt as a 2x2 panel with short one-line ticks (full
  estimand names in legend/caption) and a `[tp]` float so it stays at its citation;
  figF3 annotation split to two lines inside the plot (no right-edge clipping)
- **Frame-A**: all ten review figures regenerated in GPU-seconds (GPU-h removed from the
  partial-script chain and synced into `figures-review-src/`); A.8 keeps the measured
  6.1x serve-cost ratio beside the prose's 17x parametric-arm comparison with explicit units
- **QA infra**: `figures-qa/` rasters, manifests, and contact sheets regenerated for all
  four packages; `validate_final_visual_review.py` + index hashes updated to the current builds

Fourth-round polish (2026-08-07):
- **Worktrees**: archived + removed 7 stale Claude agent worktrees
- **Frame-A**: re-ran frozen-gate analyzer → on-disk `VERDICT:KILL`; provenance schema fixed so measured T4=0.103 is valid evidence (gate PASS); A.8 caption leads with 6.1×
- **D2**: tightened two-regime contribution wording vs Mixed/Inconclusive map
- **B6**: abstract clarifies causal confirmation is 1B primary + selected mid-scale through 3B, not a uniform ≤3B claim

## Review PDFs (read these)

| File | Package | Pages | Truth state |
|---|---|---|---|
| `D2-neurocomputing-honest-review.pdf` | D2 / Neurocomputing | 34 | Prospective mixed: P1/P2/P4 pass, P3 passes 1/3 seeds |
| `B6-ieee-tetci-honest-review.pdf` | B6 / IEEE TETCI | 14 | Revision review only; submitted artifact frozen |
| `FrameA-eswa-honest-review.pdf` | Frame-A / ESWA | 19 | Router gate KILL (0.103 < 0.5), kept visible |
| `PaperB-neurocomputing-honest-review.pdf` | Paper B / Neurocomputing | 30 | H11 complete 9/9, G-S3 PASS (ρ=-0.900), figF3 on p19 |

## Contact sheets (quick scan before opening PDFs)

- `*-pages-contact-sheet.png` — every page of each review PDF as a grid
- `*-figures-contact-sheet.png` — every in-manuscript figure as a grid

## Per-page / per-figure full-resolution PNGs

Not copied here (several hundred MB); they stay in each package's
`figures-qa/` directory next to the sources:

- `submissions/d2-neurocomputing/figures-qa/`
- `submissions/ieee/figures-qa/`
- `submissions/frame-a-eswa/figures-qa/`
- `submissions/paper-b-neurocomputing/figures-qa/`
