# Paper Visual QA Tool

Unified visual quality assurance tool for multi-package paper submissions.

## Usage

```bash
python submissions/visual_qa.py <package_dir> <pdf_path> [--status STATUS] [--refresh]
```

**Parameters:**
- `package_dir`: Package directory (e.g., `submissions/frame-a-eswa`)
- `pdf_path`: Path to PDF file
- `--status`: Optional scientific status (`candidate`, `honest-draft`, or `incomplete`)
- `--refresh`: Regenerate this package's canonical page rasters and contact sheet while preserving standalone QA assets

**Example:**
```bash
python submissions/visual_qa.py \
    submissions/d2-neurocomputing \
    submissions/d2-neurocomputing/main.pdf \
    --status honest-draft
```

## Target Packages

The tool supports all four submission packages:
- `submissions/frame-a-eswa`
- `submissions/d2-neurocomputing`
- `submissions/paper-b-neurocomputing`
- `submissions/ieee` (including `ieee/flat`)

## Outputs

Generated in `<package>/figures-qa/`:

1. **`<package>-main-page-###.png`** - 200dpi page rasters
2. **`contact-sheet.png`** - Grid overview of all pages
3. **`manifest.json`** - Machine-readable QA report
4. **`manifest.md`** - Human-readable QA report

## QA Checks

### PDF Information
- Page count, size, SHA256 hash
- Extracted via `pdfinfo`

### Font Embedding
- Total fonts and embedding status
- Flags non-embedded fonts
- Extracted via `pdffonts`

### Text Content Scan
- Detects forbidden patterns:
  - **Placeholders:** TODO, FIXME, XXX, ???
  - **Internal paths:** /home/, /Users/, edit-harness/, .omc/
  - **Codenames:** B6, E1-E9, D1-D9, MIX_A/B/C, run_*, etc.
- Extracted via `pdftotext`

### LaTeX Build
- Parses `.log` files for:
  - Errors
  - Overfull boxes
  - Undefined references

### Source Freshness
- Checks if `.tex` source files are newer than PDF
- Warns if rebuild needed

### Graphics References
- Scans `\includegraphics{}` commands
- Flags missing image files
- Searches in: package root, `figures/`, `figures-r/`, `figures-src/`, `figures-tex/`

### Page Rasters
- Generates 200dpi PNG per page
- Checks for non-empty pages
- Reuses existing files by default only when their manifest PDF SHA256 matches the selected PDF
- Refuses a different PDF build in the same package namespace unless `--refresh` is explicit
- With `--refresh`, regenerates only `<package>-main-page-###.png` files and the contact sheet

## Behavior

### Non-destructive
- Does NOT clear unrelated `figures-qa/` contents
- Does NOT overwrite existing page PNGs unless `--refresh` is explicit
- Does NOT overwrite standalone figure QA files
- Does NOT modify source files or rebuild PDFs
- Safe to run multiple times

### Standalone Figure QA
Standalone figure QA files (e.g., `fig01_*.png`) are preserved. Only package-main page rasters follow the naming pattern `<package>-main-page-###.png`.

## Testing

Run focused tests:
```bash
python -m pytest submissions/test_visual_qa.py -v
```

Tests cover:
1. Multi-page PDFs render every page to canonical filenames
2. Graceful failure when PDF not found
3. Processing a minimal fixture PDF
4. Matching-log selection for named review PDFs
5. Detecting source-newer-than-PDF
6. Detecting forbidden text patterns
7. Detecting missing graphics
8. Default non-overwriting behavior
9. Scoped `--refresh` behavior that preserves standalone QA assets
10. Different PDF builds require explicit `--refresh` before reusing the package raster namespace

## Dependencies

Standard tools (pre-installed on most Linux systems):
- `pdfinfo` (from poppler-utils)
- `pdffonts` (from poppler-utils)
- `pdftotext` (from poppler-utils)
- `pdftoppm` (from poppler-utils)
- `montage` (from ImageMagick, optional for contact sheets)

Python: standard library only (no external packages required for the tool itself; `pytest` needed for tests)

## Structure Compliance

Per `docs/STRUCTURE.md`:
- Tool: `submissions/visual_qa.py`
- Tests: `submissions/test_visual_qa.py`
- Reports: Each package's `figures-qa/` directory
- Depth: ≤4 levels (tool at level 2, reports at level 3)

## Exit Codes

- `0`: Success
- `1`: Error (PDF not found, processing failed, etc.)

## Example Output

```
Running QA for d2-neurocomputing...
Contact sheet: d2-neurocomputing/figures-qa/contact-sheet.png
JSON report: d2-neurocomputing/figures-qa/manifest.json
Markdown report: d2-neurocomputing/figures-qa/manifest.md

✓ Visual QA complete
```
