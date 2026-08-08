#!/usr/bin/env python3
"""Validate the final visual-review index and ready-package artifacts."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "FINAL-VISUAL-REVIEW-2026-08-04.md"
BANNER = "HONEST-STATE REVIEW DRAFT"

READY = (
    {
        "name": "D2",
        "package": ROOT / "d2-neurocomputing",
        "pdf": ROOT / "d2-neurocomputing" / "main-honest-review.pdf",
        "pages": 34,
        "figures": 5,
        "review_sha": "d5514f53f842735d8afb8baa65ba006a91f268fda7aa1f6ca38db721411fe6e7",
        "page_sheet_sha": "d26b46a3b4d5a69359f62d83eeb08683147d80915a762fb0c1b611ea73a8b8d8",
        "figure_sheet_sha": "95435decb10b0fa47308e112609847384736a4000c8dc4d9cc7d5710c83700b2",
        "frozen": (
            (
                ROOT / "d2-neurocomputing" / "main.pdf",
                "5c48fa92ec69138da61f29e16ffde68c48bfe375d06b1c4194a8ca61703b9a18",
            ),
        ),
    },
    {
        "name": "B6",
        "package": ROOT / "ieee",
        "pdf": ROOT / "ieee" / "flat" / "main-honest-review.pdf",
        "pages": 14,
        "figures": 7,
        "review_sha": "2099bb3873ac54857fd922a8a7b0e01db3f238c44081ae76cb788d0b6e686bd3",
        "page_sheet_sha": "dd202f8c765936dd9c4521c8fee09832e74aa3dca4f1f2a0621c852d766cd93e",
        "figure_sheet_sha": "2e53354e956ef9be02d93349a67fcf409659ebeb25e1d2a4e0e284075854b6fd",
        "frozen": (
            (
                ROOT / "ieee" / "main-as-submitted.pdf",
                "9fe0eb55adad0bf935db54188ddc8a84440f6df8482de3f3259212830bff5145",
            ),
            (
                ROOT / "ieee" / "flat" / "TETCI_main_manuscript.zip",
                "cad4851f6b792ada599e7c6a38c309ebe0d754763f87e8ac5ce4430c33f9f0c8",
            ),
        ),
    },
    {
        "name": "Frame-A",
        "package": ROOT / "frame-a-eswa",
        "pdf": ROOT / "frame-a-eswa" / "main-honest-review.pdf",
        "pages": 19,
        "figures": 10,
        "review_sha": "ce7a18e8891d3337b0aac0b0ae9d172a4b50ab4cbc4f9e7ffbc5a5833ffb10f5",
        "page_sheet_sha": "deadf0aae94d90c1af9f2a13280f69423b3f709a7af982d8350539063511039b",
        "figure_sheet_sha": "f266fd9e5ddf2dfee9dc8aa8397c79cd5de4fe75d03e752887c4981eda72f4fc",
        "frozen": (
            (
                ROOT / "frame-a-eswa" / "main.pdf",
                "a16063536e1a318aee25104c7c6526e2201d1d369a1316cfc9b90c3bbefa673b",
            ),
        ),
    },
    {
        "name": "PaperB",
        "package": ROOT / "paper-b-neurocomputing",
        "pdf": ROOT / "paper-b-neurocomputing" / "main-honest-review.pdf",
        "pages": 30,
        "figures": 5,
        "review_sha": "a7f12ecb7c55e76314deaaac532ca450de10bad66615a4970f37fe914d5aff03",
        "page_sheet_sha": "9dfd3218b75b869964dfb2e78e3e7b2bf280f8de50563cdd262c4713d957a4f7",
        "figure_sheet_sha": "9056431483b717280ea98910d4e92edfe25db20a7366c8d98941420d5ec6f0a3",
        "frozen": (
            (
                ROOT / "paper-b-neurocomputing" / "main.pdf",
                "a40377c17e3ae559cf37c701803c3b3a098849cfe47a3cf211aaa284cbbf5c9d",
            ),
        ),
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_under(root: Path, name: str) -> Path:
    """Resolve name under root; reject absolute paths and `..` escapes."""
    root = root.resolve()
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"path escapes root: {name}")
    candidate = (root / rel).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError(f"path escapes root: {name}")
    return candidate


def pdf_text(path: Path, first_page_only: bool = False) -> str:
    command = ["pdftotext"]
    if first_page_only:
        command.extend(["-f", "1", "-l", "1"])
    command.extend([str(path), "-"])
    return subprocess.check_output(command, text=True)


def main() -> None:
    index_text = INDEX.read_text()
    for spec in READY:
        package = spec["package"]
        qa = package / "figures-qa"
        manifest = json.loads((qa / "manifest.json").read_text())
        figure_manifest = json.loads((qa / "figures-manifest.json").read_text())

        assert spec["pdf"].is_file(), spec["pdf"]
        manifest_pdf = Path(manifest["pdf_path"])
        if not manifest_pdf.is_absolute():
            manifest_pdf = ROOT.parent / manifest_pdf
        assert manifest_pdf.resolve() == spec["pdf"].resolve()
        assert manifest["checks"]["pdf_info"]["data"]["sha256"] == spec["review_sha"]
        assert sha256(spec["pdf"]) == spec["review_sha"]
        assert manifest["checks"]["pages"]["total_pages"] == spec["pages"]
        assert len(manifest["checks"]["pages"]["pages"]) == spec["pages"]
        assert not manifest["checks"]["pages"]["empty_pages"]
        assert figure_manifest["count"] == spec["figures"]
        assert len(figure_manifest["figures"]) == spec["figures"]
        assert sha256(qa / "contact-sheet.png") == spec["page_sheet_sha"]
        assert sha256(qa / "figures-contact-sheet.png") == spec["figure_sheet_sha"]
        assert BANNER in pdf_text(spec["pdf"], first_page_only=True)
        assert spec["review_sha"] in index_text
        assert spec["page_sheet_sha"] in index_text
        assert spec["figure_sheet_sha"] in index_text

        for page in manifest["checks"]["pages"]["pages"]:
            raster = safe_under(qa, page["file"])
            assert raster.is_file() and raster.stat().st_size > 1000, raster
        for figure in figure_manifest["figures"]:
            raster = safe_under(qa, figure["png"])
            assert raster.is_file() and raster.stat().st_size == figure["bytes"], raster
            assert sha256(raster) == figure["sha256"]

        for frozen_path, frozen_sha in spec["frozen"]:
            assert frozen_path.is_file(), frozen_path
            assert sha256(frozen_path) == frozen_sha
            assert frozen_sha in index_text

        print(f"{spec['name']}: {spec['pages']} pages, {spec['figures']} figures, hashes verified")


if __name__ == "__main__":
    main()
