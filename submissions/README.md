# Submissions — per-venue workspaces (created 2026-07-05)

> One paper core, multiple potential venues, target NOT yet decided. Each venue gets its
> own workspace so drafts never cross-contaminate. SHARED TRUTH lives outside these dirs:
> canonical numbers = `../edit-harness/results/*.json`; figures = package-local `figures-src/` and `figures-qa/` outputs regenerated from those results; binding wording = `../docs/findings/*.md` and `../CLAUDE.md`; number macros follow each package's local source.
> RULE: a venue workspace may COPY from shared truth, never the reverse; any new number
> enters shared truth (canonical JSON + review gate) first.

## Workspaces
- `paper-arr/` — historical ARR package; **not present in this checkout** after the journal-first pivot. The old 2026-08-03 cycle notes are historical only.
- `ieee/` — **BUILT (2026-07-05, sonnet workflow)**: IEEEtran journal package, double-column,
  13pp compiled (target ~14 incl. extension work). Venue fork `\iftnnls`/`\iftaslp` in
  main.tex; 6 disclosed EXTENSION stubs (theorem, 8B causal, 6th editor, EGL seeds,
  dataset breadth); macros byte-identical to paper-arr; IEEE-width R figures. Leak-swept
  (verifier caught 6 caption filename leaks — fixed + re-verified 0). See `ieee/SETUP.md`
  + `ieee/VENUE-NOTE.md`. Authors = placeholder (journals not anonymous — fill at venue
  decision).
- `kbs/` — Knowledge-Based Systems (Elsevier, SCIE Q1). elsarticle format, no page limit,
  ROLLING submission. See `kbs/EXTENSION-PLAN.md` for the gap list.
- `tnnls/` — IEEE TNNLS (SCIE Q1, CCF-B journal). IEEEtran format, rolling. Higher bar:
  theory/artifact expectation. See `tnnls/EXTENSION-PLAN.md`.

## Standing constraints (from CLAUDE.md / venue strategy — apply to ALL venues)
> The current workspace policy is **SCIE-indexed**. CCF rank is not required. TMLR, BlackboxNLP, ICBINB, COLM, and EACL fail the current filter. Historical package notes below may preserve older venue-planning language; they are not current submission instructions.
- Dual-submission rules: the SAME content cannot be under review at a journal and ARR
  simultaneously. The sanctioned path (VENUE-GAP-ANALYSIS 2026-07-01/02): ARR first,
  journal EXTENSION after with substantial new material (norm: ≥30% new content +
  disclosure of the conference version). A journal-FIRST path is possible instead —
  see the timing comparison in the extension plans — but forfeits the Aug-3 ARR cycle.
- Author/review separate passes; every quoted number verified against canonical JSON.

---

## Version discipline — canonical PDF per package (updated 2026-08-05)

> RULE: Open the correct PDF for the task. Wrong PDF = wrong truth.

| Package | **Open for reading/review** | Frozen submission (read-only) | Do NOT open as current truth |
|---|---|---|---|
| **Frame-A / ESWA** | `frame-a-eswa/main-honest-review.pdf` (19pp) | — not yet submitted | `frame-a-eswa/main.pdf` — placeholder稿，图已过时 |
| **D2 / Neurocomputing** | `d2-neurocomputing/main-honest-review.pdf` (34pp) | `d2-neurocomputing/main.submitted-20260717.pdf` | `d2-neurocomputing/main.pdf` — 提交前稿 |
| **B6 / IEEE TETCI** | `ieee/revision/tetci-corrected-20260808/main.pdf` (14pp) | `ieee/flat/main.pdf` ← **冻结件，绝不修改** | `ieee/flat/main-honest-review.pdf` — historical QA artifact; `ieee/main.pdf` — live hierarchical build (15pp, bibliography spill) |
| **Paper B / Neurocomputing** | `paper-b-neurocomputing/main-honest-review.pdf` (30pp) | — not yet submitted | `paper-b-neurocomputing/main.pdf` — 不含 figF3 (H11图) |

### Orphaned / isolated files

| Path | Contents | Status |
|---|---|---|
| `d2-neurocomputing/figures-src/ORPHAN/` | 16 expanded panel PDFs (figF1A–figF8D) + make_figures_d2_expanded.R | Isolated 2026-08-05; not referenced by manuscript |
| `ieee/figures-src/ORPHAN/` | figF1.pdf, figF1_fixed.pdf, figF8.pdf, figF8_fixed.pdf + aux/log | Isolated 2026-08-05; manuscript uses tikzDevice chain only |
| `d2-federation/` | Historical federation submission package | Reference only; deposit = d2-neurocomputing |
| `paper-arr/` | B6 ARR package (11pp, 2026-07-06) | Shelved (journal-first pivot); not current |

### 2026-08-05 figure repair campaign summary

- **Frame-A**: eliminated all literal `NA` from figures (R factor-label fix); populated figF8c; fixed figF5 clipping and figF7/F1 label overlap; unified GPU axis units to GPU-s (08-06: GPU-h removed from the partial-script chain and review inputs)
- **Paper B**: fig02 Panel D unified to ROME blue; fig04c y-axis limit→80; "KILLED" → "does not survive its pre-registered gate"; fig03 x-axis labels added; fig06_width_law restored as Appendix figure
- **B6/IEEE**: old figure variants moved to ORPHAN/; Index Terms intact (no truncation); 0 overfull
- **D2**: expanded panels moved to ORPHAN/; p1 has full title+abstract (not blank); 1 overfull 2.61pt (float placement, not visually noticeable)
