# Final Visual Review Index — 2026-08-04

This index is for visual inspection only. Every review PDF must display
`HONEST-STATE REVIEW DRAFT — NOT SUBMISSION CANDIDATE` on page 1. Frozen or
previously submitted artifacts remain separate and are not replaced by these files.

## Package status

| Package | Review state | Review PDF | Full-page QA | In-manuscript figure QA |
|---|---|---|---|---|
| D2 / Neurocomputing | READY FOR VISUAL REVIEW; prospective result remains mixed (P3 passes 1/3) | `d2-neurocomputing/main-honest-review.pdf` | `d2-neurocomputing/figures-qa/contact-sheet.png` (34 pages) | `d2-neurocomputing/figures-qa/figures-contact-sheet.png` (5 composite figures) |
| B6 / IEEE TETCI | READY FOR VISUAL REVIEW; revision review only, submitted artifact frozen | `ieee/flat/main-honest-review.pdf` | `ieee/figures-qa/contact-sheet.png` (14 pages) | `ieee/figures-qa/figures-contact-sheet.png` (7 figures) |
| Frame-A / ESWA | READY FOR VISUAL REVIEW; preregistered router gate is KILL (`0.103 < 0.5`) | `frame-a-eswa/main-honest-review.pdf` | `frame-a-eswa/figures-qa/contact-sheet.png` (19 pages) | `frame-a-eswa/figures-qa/figures-contact-sheet.png` (10 figures) |
| Paper B / Neurocomputing | READY FOR VISUAL REVIEW; H11 complete (9/9 cells), G-S3 PASS ($\rho=-0.900$) | `paper-b-neurocomputing/main-honest-review.pdf` | `paper-b-neurocomputing/figures-qa/contact-sheet.png` (30 pages) | `paper-b-neurocomputing/figures-qa/figures-contact-sheet.png` (5 manuscript figures) |

## D2 / Neurocomputing

- Scientific status: honest-state review draft; not a submission candidate.
- Boundary: P1/P2/P4 pass; P3 passes 1/3 seeds; full confirmation is blocked.
- PDF manifest: `d2-neurocomputing/figures-qa/manifest.json`
- Figure manifest: `d2-neurocomputing/figures-qa/figures-manifest.json`
- Review PDF SHA256: `d5514f53f842735d8afb8baa65ba006a91f268fda7aa1f6ca38db721411fe6e7`.
- Full-page contact sheet SHA256: `d26b46a3b4d5a69359f62d83eeb08683147d80915a762fb0c1b611ea73a8b8d8`.
- In-manuscript figure contact sheet SHA256: `95435decb10b0fa47308e112609847384736a4000c8dc4d9cc7d5710c83700b2`.
- Frozen `main.pdf` SHA256: `5c48fa92ec69138da61f29e16ffde68c48bfe375d06b1c4194a8ca61703b9a18`.
- Automated checks: fonts embedded; text/path leak scan clean; 0 LaTeX errors;
  0 undefined references; one 2.61108 pt overfull warning retained for visual review.

## B6 / IEEE TETCI

- Scientific status: honest-state revision review draft; not a submission candidate.
- Boundary: SxC is an exact rank-one reduction, not a faithful true-influence rank
  surrogate; signed law is Llama-family scoped; strong causal law is not claimed at scale.
- PDF manifest: `ieee/figures-qa/manifest.json`
- Figure manifest: `ieee/figures-qa/figures-manifest.json`
- Review PDF SHA256: `2099bb3873ac54857fd922a8a7b0e01db3f238c44081ae76cb788d0b6e686bd3`.
- Full-page contact sheet SHA256: `dd202f8c765936dd9c4521c8fee09832e74aa3dca4f1f2a0621c852d766cd93e`.
- In-manuscript figure contact sheet SHA256: `2e53354e956ef9be02d93349a67fcf409659ebeb25e1d2a4e0e284075854b6fd`.
- Automated checks: fonts embedded; text/path leak scan clean; 0 LaTeX errors;
  0 undefined references; seven 0.94–1.45 pt figure overfull warnings retained for visual review.
- Frozen `main-as-submitted.pdf` SHA256:
  `9fe0eb55adad0bf935db54188ddc8a84440f6df8482de3f3259212830bff5145`.
- Frozen `flat/TETCI_main_manuscript.zip` SHA256:
  `cad4851f6b792ada599e7c6a38c309ebe0d754763f87e8ac5ce4430c33f9f0c8`.

## Frame-A / ESWA

- Scientific status: honest-state review draft; not a submission candidate.
- Boundary: the preregistered router gate is **KILL**; T4 is `0.103 < 0.5`.
  The review copy keeps the measured KILL outcome and does not launder it into PASS.
- PDF manifest: `frame-a-eswa/figures-qa/manifest.json`
- Figure manifest: `frame-a-eswa/figures-qa/figures-manifest.json`
- Review PDF SHA256: `ce7a18e8891d3337b0aac0b0ae9d172a4b50ab4cbc4f9e7ffbc5a5833ffb10f5`.
- Full-page contact sheet SHA256: `deadf0aae94d90c1af9f2a13280f69423b3f709a7af982d8350539063511039b`.
- In-manuscript figure contact sheet SHA256: `f266fd9e5ddf2dfee9dc8aa8397c79cd5de4fe75d03e752887c4981eda72f4fc`.
- Frozen `main.pdf` SHA256: `a16063536e1a318aee25104c7c6526e2201d1d369a1316cfc9b90c3bbefa673b`.
- Automated checks: 19 nonblank pages, 10 nonblank standalone figures, all fonts embedded,
  0 LaTeX errors, 0 undefined references, 0 overfull boxes, and 0 missing graphics for
  the selected honest-review source. The generic text scan reports two uses of
  “placeholder” in explicit negations (“not a placeholder” and “synthetic-cost
  placeholders”), not unfinished artifacts.

## Paper B / Neurocomputing

- Scientific status: honest-state review draft; not a submission candidate.
- Boundary: H11 replication grid complete (gemma2b L19, qwen3b L27, phi35 L24 × 3 seeds);
  G-S3 PASS with $\rho=-0.900$ (threshold $-0.3$) on the 9-cell NEW grid.
  Phi-3.5 s2 was recovered from box 36039 (out_dir misplacement fixed, pair validated).
  Llama-3.2-3B L24 s1 ran as a parallel supplementary cell (table only, npz overwritten
  by phi35 s2 sharing the same out_dir — known limitation, not part of the 9-cell gate).
- PDF manifest: `paper-b-neurocomputing/figures-qa/manifest.json`
- Figure manifest: `paper-b-neurocomputing/figures-qa/figures-manifest.json`
- Review PDF SHA256: `a7f12ecb7c55e76314deaaac532ca450de10bad66615a4970f37fe914d5aff03`.
- Full-page contact sheet SHA256: `9dfd3218b75b869964dfb2e78e3e7b2bf280f8de50563cdd262c4713d957a4f7`.
- In-manuscript figure contact sheet SHA256: `9056431483b717280ea98910d4e92edfe25db20a7366c8d98941420d5ec6f0a3`.
- Frozen `main.pdf` SHA256: `a40377c17e3ae559cf37c701803c3b3a098849cfe47a3cf211aaa284cbbf5c9d`.
- Automated checks: 30 pages, 0 LaTeX errors, 0 undefined references, 0 overfull boxes.
  figF3 (noise-to-signal vs rank survival, 18 cells, 4 families) inserted after
  Table 2 in §6.2; G-S3 PASS annotation rendered in-figure.


   clipping, and legibility.
2. Open each full-page `contact-sheet.png` and inspect float placement, blank space,
   headings, tables, and banner placement.
3. Use the per-page PNGs in the same `figures-qa/` directory for any page that needs
   full-resolution inspection.
4. Read `manifest.md` for the build-warning counts and `manifest.json` for PDF SHA256,
   exact page list, font status, and leak-scan result.
