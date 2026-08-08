#!/usr/bin/env python3
"""
Focused tests for visual_qa.py

Tests:
1. Fails gracefully when PDF not found
2. Processes a minimal fixture PDF
3. Detects source-newer-than-PDF
4. Detects forbidden text patterns
5. Detects missing graphics references
"""

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import pytest


VISUAL_QA = Path(__file__).with_name("visual_qa.py").resolve()


@pytest.fixture
def temp_package():
    """Create temporary package directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        pkg_dir = Path(tmpdir) / "test-package"
        pkg_dir.mkdir()
        yield pkg_dir


@pytest.fixture
def minimal_pdf(temp_package):
    """Create minimal PDF fixture using pdflatex."""
    tex_content = r"""
\documentclass{article}
\begin{document}
Hello World
\end{document}
"""
    tex_file = temp_package / "minimal.tex"
    tex_file.write_text(tex_content)

    # Compile to PDF
    subprocess.run(
        ["pdflatex", "-interaction=batchmode", str(tex_file)],
        cwd=temp_package,
        capture_output=True
    )

    pdf_file = temp_package / "minimal.pdf"
    assert pdf_file.exists(), "PDF fixture creation failed"
    return pdf_file


@pytest.fixture
def multipage_pdf(temp_package):
    """Create a three-page PDF fixture to lock per-page raster behavior."""
    tex_content = r"""
\documentclass{article}
\begin{document}
Page one\newpage
Page two\newpage
Page three
\end{document}
"""
    tex_file = temp_package / "multipage.tex"
    tex_file.write_text(tex_content)
    subprocess.run(
        ["pdflatex", "-interaction=batchmode", str(tex_file)],
        cwd=temp_package,
        capture_output=True,
        check=True,
    )
    pdf_file = temp_package / "multipage.pdf"
    assert pdf_file.exists(), "Multi-page PDF fixture creation failed"
    return pdf_file


def test_multipage_fixture_renders_every_page(temp_package, multipage_pdf):
    """A multi-page PDF must yield one canonical PNG per page, with no suffix debris."""
    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(multipage_pdf),
            "--status", "honest-draft",
        ],
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert result.returncode == 0, result.stderr

    qa_dir = temp_package / "figures-qa"
    page_pngs = sorted(qa_dir.glob("test-package-main-page-*.png"))
    assert [p.name for p in page_pngs] == [
        "test-package-main-page-001.png",
        "test-package-main-page-002.png",
        "test-package-main-page-003.png",
    ]
    assert all(p.stat().st_size > 1000 for p in page_pngs)

    data = json.loads((qa_dir / "manifest.json").read_text())
    pages = data["checks"]["pages"]
    assert pages["status"] == "ok"
    assert pages["total_pages"] == 3
    assert pages["generated"] == 3
    assert not list(qa_dir.glob("test-package-main-page-*-*.png"))


def test_pdf_not_found(temp_package):
    """Test graceful failure when PDF doesn't exist."""
    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(temp_package / "nonexistent.pdf")
        ],
        capture_output=True,
        text=True
    )

    assert result.returncode != 0, "Should fail when PDF not found"
    assert "not found" in result.stderr.lower(), "Should report missing PDF"


def test_minimal_fixture(temp_package, minimal_pdf):
    """Test processing a minimal fixture PDF."""
    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf),
            "--status", "honest-draft"
        ],
        capture_output=True,
        text=True,
        cwd="."
    )

    assert result.returncode == 0, f"Should succeed on valid PDF\nStderr: {result.stderr}"

    # Check outputs exist
    qa_dir = temp_package / "figures-qa"
    assert qa_dir.exists(), "figures-qa directory should be created"

    manifest_json = qa_dir / "manifest.json"
    assert manifest_json.exists(), "manifest.json should be created"

    manifest_md = qa_dir / "manifest.md"
    assert manifest_md.exists(), "manifest.md should be created"

    # Check at least one page PNG
    page_pngs = list(qa_dir.glob("test-package-main-page-*.png"))
    assert len(page_pngs) >= 1, "At least one page PNG should be generated"

    # Verify JSON structure
    with open(manifest_json) as f:
        data = json.load(f)

    assert data["package"] == "test-package"
    assert data["status"] == "honest-draft"
    assert "checks" in data
    assert "pdf_info" in data["checks"]
    assert "pages" in data["checks"]

    # Check page is non-empty
    pages_check = data["checks"]["pages"]
    assert pages_check["status"] in ["ok", "warning"]
    assert pages_check["total_pages"] >= 1


def test_review_pdf_uses_only_matching_log(temp_package, minimal_pdf):
    """Review copies must not inherit warnings from an unrelated main.log."""
    review_pdf = temp_package / "revision-review.pdf"
    shutil.copy2(minimal_pdf, review_pdf)
    (temp_package / "main.log").write_text("Overfull \\hbox (99.0pt too wide)\n")

    result = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(review_pdf)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads((temp_package / "figures-qa" / "manifest.json").read_text())
    assert data["checks"]["latex"]["status"] == "skip"

    (temp_package / "revision-review.log").write_text(
        "This is pdfTeX.\nOutput written on revision-review.pdf (1 page).\n"
    )
    result = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(review_pdf)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads((temp_package / "figures-qa" / "manifest.json").read_text())
    latex = data["checks"]["latex"]
    assert latex["status"] == "ok"
    assert latex["log_file"] == "revision-review.log"


def test_source_newer_than_pdf(temp_package, minimal_pdf):
    """Test detection when the source associated with the PDF is newer."""
    tex_file = temp_package / "minimal.tex"

    time.sleep(0.1)  # Ensure timestamp difference
    tex_file.touch()

    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf)
        ],
        capture_output=True,
        text=True,
        cwd="."
    )

    assert result.returncode == 0

    # Check manifest reports newer source
    manifest_json = temp_package / "figures-qa" / "manifest.json"
    with open(manifest_json) as f:
        data = json.load(f)

    freshness = data["checks"]["source_freshness"]
    assert freshness["status"] == "warning", "Should warn about newer sources"
    assert any("minimal.tex" in s for s in freshness["newer_sources"])


def test_forbidden_text_patterns(temp_package):
    """Test detection of forbidden text patterns in PDF."""
    # Create PDF with forbidden patterns
    tex_content = r"""
\documentclass{article}
\begin{document}
This is a TODO item.
Path: /home/user/project/file.txt
Codename: B6 experiment
\end{document}
"""
    tex_file = temp_package / "forbidden.tex"
    tex_file.write_text(tex_content)

    subprocess.run(
        ["pdflatex", "-interaction=batchmode", str(tex_file)],
        cwd=temp_package,
        capture_output=True
    )

    pdf_file = temp_package / "forbidden.pdf"
    assert pdf_file.exists()

    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(pdf_file)
        ],
        capture_output=True,
        text=True,
        cwd="."
    )

    assert result.returncode == 0

    # Check manifest reports forbidden patterns
    manifest_json = temp_package / "figures-qa" / "manifest.json"
    with open(manifest_json) as f:
        data = json.load(f)

    text_scan = data["checks"]["text_scan"]
    assert text_scan["status"] == "warning", "Should warn about forbidden patterns"
    assert "placeholder" in text_scan["hits"]
    assert "internal_path" in text_scan["hits"]
    assert "codename" in text_scan["hits"]


def test_missing_graphics(temp_package, minimal_pdf):
    """Test detection of missing includegraphics references."""
    # Create .tex with missing graphic reference
    tex_file = temp_package / "main.tex"
    tex_file.write_text(r"""
\documentclass{article}
\usepackage{graphicx}
\begin{document}
\includegraphics{missing-figure}
\end{document}
""")

    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf)
        ],
        capture_output=True,
        text=True,
        cwd="."
    )

    assert result.returncode == 0

    # Check manifest reports missing graphic
    manifest_json = temp_package / "figures-qa" / "manifest.json"
    with open(manifest_json) as f:
        data = json.load(f)

    graphics = data["checks"]["graphics"]
    assert graphics["status"] == "warning", "Should warn about missing graphics"
    assert graphics["missing_count"] > 0
    assert any("missing-figure" in m["graphic"] for m in graphics["missing"])


def test_does_not_overwrite_existing(temp_package, minimal_pdf):
    """Test that existing figures-qa files are not overwritten."""
    # Run once
    subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf)
        ],
        capture_output=True,
        cwd="."
    )

    # Find generated page PNG
    qa_dir = temp_package / "figures-qa"
    page_pngs = list(qa_dir.glob("test-package-main-page-*.png"))
    assert len(page_pngs) >= 1

    first_png = page_pngs[0]
    original_mtime = first_png.stat().st_mtime

    time.sleep(0.1)

    # Run again
    subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf)
        ],
        capture_output=True,
        cwd="."
    )

    # Check that file was not regenerated
    new_mtime = first_png.stat().st_mtime
    assert new_mtime == original_mtime, "Should not overwrite existing page PNG"

    # Check manifest reports as "existing"
    manifest_json = qa_dir / "manifest.json"
    with open(manifest_json) as f:
        data = json.load(f)

    pages = data["checks"]["pages"]
    assert any(p["status"] == "existing" for p in pages["pages"])


def test_refresh_overwrites_only_canonical_pages(temp_package, minimal_pdf):
    """Refresh regenerates page rasters while preserving standalone QA assets."""
    result = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(minimal_pdf)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    qa_dir = temp_package / "figures-qa"
    page_png = next(qa_dir.glob("test-package-main-page-*.png"))
    standalone = qa_dir / "standalone-figure.png"
    standalone.write_bytes(b"preserve-me")
    page_mtime = page_png.stat().st_mtime_ns

    time.sleep(0.1)
    result = subprocess.run(
        [
            "python",
            str(VISUAL_QA),
            str(temp_package),
            str(minimal_pdf),
            "--refresh",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert page_png.stat().st_mtime_ns > page_mtime
    assert standalone.read_bytes() == b"preserve-me"

    data = json.loads((qa_dir / "manifest.json").read_text())
    assert data["refresh"] is True
    assert data["checks"]["pages"]["generated"] == 1
    assert data["checks"]["pages"]["existing"] == 0


def test_different_pdf_requires_explicit_refresh(temp_package, minimal_pdf):
    """A second PDF build cannot silently reuse canonical rasters from the first."""
    first = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(minimal_pdf)],
        capture_output=True,
        text=True,
    )
    assert first.returncode == 0

    qa_dir = temp_package / "figures-qa"
    page_png = next(qa_dir.glob("test-package-main-page-*.png"))
    original_mtime = page_png.stat().st_mtime_ns
    original = json.loads((qa_dir / "manifest.json").read_text())
    original_sha = original["checks"]["pdf_info"]["data"]["sha256"]

    second_tex = temp_package / "second.tex"
    second_tex.write_text(
        r"\documentclass{article}\begin{document}Different PDF\end{document}"
    )
    subprocess.run(
        ["pdflatex", "-interaction=batchmode", str(second_tex)],
        cwd=temp_package,
        capture_output=True,
        check=True,
    )
    second_pdf = temp_package / "second.pdf"

    rejected = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(second_pdf)],
        capture_output=True,
        text=True,
    )
    assert rejected.returncode == 1
    assert "different PDF build" in rejected.stderr
    assert page_png.stat().st_mtime_ns == original_mtime
    after_reject = json.loads((qa_dir / "manifest.json").read_text())
    assert after_reject["checks"]["pdf_info"]["data"]["sha256"] == original_sha

    time.sleep(0.1)
    refreshed = subprocess.run(
        ["python", str(VISUAL_QA), str(temp_package), str(second_pdf), "--refresh"],
        capture_output=True,
        text=True,
    )
    assert refreshed.returncode == 0
    assert page_png.stat().st_mtime_ns > original_mtime
    after_refresh = json.loads((qa_dir / "manifest.json").read_text())
    assert after_refresh["checks"]["pdf_info"]["data"]["sha256"] != original_sha


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
