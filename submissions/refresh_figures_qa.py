#!/usr/bin/env python3
"""Regenerate per-package figure QA artifacts (figure-*.png rasters,
figures-manifest.json, figures-contact-sheet.png).

Frame-A figures are tikzDevice fragments consumed by the manuscript, so each is
compiled standalone from figures-review-src/ (the manuscript's actual inputs).
Paper B figures are pre-compiled PDFs in figures/ (the manuscript includes them).
B6/D2 are not touched here; their figure artifacts are managed separately.

Usage: python3 refresh_figures_qa.py [frame-a-eswa|paper-b-neurocomputing ...]
"""

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent

STANDALONE_WRAPPER = r"""\documentclass[border=2pt]{{standalone}}
\usepackage{{tikz}}
\usepackage{{xcolor}}
\begin{{document}}
\input{{{tex}}}
\end{{document}}
"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rasterize_pdf(pdf: Path, png: Path) -> None:
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", "-singlefile", str(pdf), str(png.with_suffix(""))],
        check=True, capture_output=True,
    )


def rasterize_tikz(tex: Path, png: Path, workdir: Path) -> None:
    wrapper = workdir / f"{tex.stem}_wrap.tex"
    wrapper.write_text(STANDALONE_WRAPPER.format(tex=tex))
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-output-directory={workdir}", str(wrapper)],
        check=True, capture_output=True,
    )
    rasterize_pdf(workdir / f"{tex.stem}_wrap.pdf", png)


def image_geometry(path: Path):
    try:
        with Image.open(path) as im:
            return im.width, im.height
    except OSError:
        return None


def nonwhite_fraction(path: Path):
    try:
        with Image.open(path) as im:
            hist = im.convert("L").histogram()
        total = sum(hist)
        if total <= 0:
            return None
        return round(sum(hist[0:250]) / total, 6)
    except OSError:
        return None


def contact_sheet(pngs, out: Path) -> None:
    subprocess.run(
        ["montage", *[str(p) for p in pngs], "-tile", "2x", "-geometry", "+4+4",
         "-background", "white", str(out)],
        check=True, capture_output=True,
    )


def refresh_frame_a() -> dict:
    pkg = ROOT / "frame-a-eswa"
    qa = pkg / "figures-qa"
    src = pkg / "figures-review-src"
    figures = []
    with tempfile.TemporaryDirectory() as tmp:
        for tex in sorted(src.glob("figF*.tex")):
            png = qa / f"figure-{tex.stem}.png"
            rasterize_tikz(tex, png, Path(tmp))
            dims = image_geometry(png)
            entry = {
                "png": png.name,
                "bytes": png.stat().st_size,
                "sha256": sha256(png),
            }
            if dims:
                entry["width"], entry["height"] = dims
            frac = nonwhite_fraction(png)
            if frac is not None:
                entry["nonwhite_fraction"] = frac
                entry["blank"] = frac < 0.001
            figures.append(entry)
    sheet = qa / "figures-contact-sheet.png"
    contact_sheet([qa / f["png"] for f in figures], sheet)
    manifest = {"count": len(figures), "figures": figures}
    (qa / "figures-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def refresh_paper_b() -> dict:
    pkg = ROOT / "paper-b-neurocomputing"
    qa = pkg / "figures-qa"
    old = json.loads((qa / "figures-manifest.json").read_text())
    sources = [
        ("fig01_codec_scope", "figures/fig01_codec_scope.pdf"),
        ("fig02_efficacy_survival", "figures/fig02_efficacy_survival.pdf"),
        ("fig03_rank_survival", "figures/fig03_rank_survival.pdf"),
        ("fig04_reconstruction_gap", "figures/fig04_reconstruction_gap.pdf"),
        ("figF3_noise_signal_rank_survival", "figures/figF3_noise_signal_rank_survival.pdf"),
    ]
    figures = []
    for name, source in sources:
        pdf = pkg / source
        png = qa / f"figure-{name}.png"
        rasterize_pdf(pdf, png)
        dims = image_geometry(png)
        figures.append({
            "name": name,
            "source": source,
            "png": png.name,
            "dimensions": f"{dims[0]}x{dims[1]}" if dims else "unknown",
            "bytes": png.stat().st_size,
            "sha256": sha256(png),
        })
    sheet = qa / "figures-contact-sheet.png"
    contact_sheet([qa / f["png"] for f in figures], sheet)
    manifest = {
        "schema_version": old.get("schema_version", 1),
        "selection": old.get("selection", "manuscript body + appendix figures"),
        "count": len(figures),
        "figures": figures,
        "contact_sheet": "figures-contact-sheet.png",
        "contact_sheet_sha256": sha256(sheet),
    }
    (qa / "figures-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def refresh_d2() -> dict:
    """Rasterize active manuscript figures figA–figE from figures-src/."""
    pkg = ROOT / "d2-neurocomputing"
    qa = pkg / "figures-qa"
    sources = [f"figures-src/fig{letter}.pdf" for letter in "ABCDE"]
    figures = []
    for source in sources:
        pdf = pkg / source
        name = Path(source).stem
        png = qa / f"figure-{name}.png"
        rasterize_pdf(pdf, png)
        dims = image_geometry(png)
        figures.append({
            "name": name,
            "source": source,
            "png": png.name,
            "dimensions": f"{dims[0]}x{dims[1]}" if dims else "unknown",
            "bytes": png.stat().st_size,
            "sha256": sha256(png),
        })
    sheet = qa / "figures-contact-sheet.png"
    contact_sheet([qa / f["png"] for f in figures], sheet)
    manifest = {
        "schema_version": 1,
        "selection": "manuscript body figA–figE",
        "count": len(figures),
        "figures": figures,
        "contact_sheet": "figures-contact-sheet.png",
        "contact_sheet_sha256": sha256(sheet),
    }
    (qa / "figures-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main() -> int:
    targets = sys.argv[1:] or ["frame-a-eswa", "paper-b-neurocomputing", "d2-neurocomputing"]
    for target in targets:
        if target == "frame-a-eswa":
            manifest = refresh_frame_a()
        elif target == "paper-b-neurocomputing":
            manifest = refresh_paper_b()
        elif target == "d2-neurocomputing":
            manifest = refresh_d2()
        else:
            print(f"unsupported package: {target}", file=sys.stderr)
            return 1
        print(f"{target}: {manifest['count']} figure rasters refreshed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
