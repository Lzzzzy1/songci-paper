#!/usr/bin/env python3
"""Verify the frozen Song Ci manuscript package using the standard library."""

from __future__ import annotations

import csv
import hashlib
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256"
REQUIRED = {
    "manuscript/final/SongCi_AICSS2026_Final_Anonymous.docx",
    "manuscript/final/SongCi_AICSS2026_Final_Anonymous.pdf",
    "manuscript/final/SongCi_AICSS2026_Final_Author_Copy.docx",
    "manuscript/final/SongCi_AICSS2026_Final_Author_Copy.pdf",
    "manuscript/README.md",
    "data/table1_corpus_flow.csv",
    "data/table2_candidate_choice_audit.csv",
    "data/table3_bounded_cases.csv",
    "references/REFERENCES.md",
    "docs/METHODS_AND_DATA.md",
    "docs/REPRODUCIBILITY.md",
    "audit/INTERNAL_QA.md",
    "audit/INTERNAL_QA.json",
    "audit/citation-verification.json",
    "README.md",
    ".gitattributes",
    ".gitignore",
    "scripts/verify_package.py",
}
TEXT_SUFFIXES = {".md", ".json", ".csv", ".py", ".txt", ".yml", ".yaml"}
IDENTITY_TOKENS = (
    b"Lin Zhanyi",
    b"Zhanyi Lin",
    b"Hong Kong Metropolitan University",
    b"lzzzy20041125",
    b"@outlook.com",
)
PROJECT_MARKERS = (
    ("adap" + "tabprompt").encode(),
    ("yo" + "lo").encode(),
    ("research" + "-papers").encode(),
)
SECRET_PATTERNS = (
    re.compile(("gh" + "o_[A-Za-z0-9]{20,}").encode()),
    re.compile(("github" + "_pat_[A-Za-z0-9_]{20,}").encode()),
    re.compile(("sk" + "-[A-Za-z0-9_-]{20,}").encode()),
    re.compile(("AKIA" + "[A-Z0-9]{16}").encode()),
    re.compile(("-----BEGIN " + "(?:RSA |EC |OPENSSH )?PRIVATE KEY-----").encode()),
)
NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}
W = "{" + NS["w"] + "}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().lower()


def package_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or ".git" in path.parts
            or "__pycache__" in path.parts
            or path.suffix.lower() in {".pyc", ".pyo"}
        ):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel != MANIFEST.name:
            files.add(rel)
    return files


def parse_manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    if not MANIFEST.is_file():
        raise FileNotFoundError("MANIFEST.sha256 is missing")
    for line_no, line in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})  (.+)", line)
        if not match:
            raise ValueError(f"invalid manifest line {line_no}: {line!r}")
        rel = match.group(2).replace("\\", "/")
        candidate = (ROOT / rel).resolve()
        if ROOT.resolve() not in candidate.parents:
            raise ValueError(f"unsafe manifest path: {rel}")
        if rel in entries:
            raise ValueError(f"duplicate manifest path: {rel}")
        entries[rel] = match.group(1).lower()
    return entries


def docx_payload(path: Path) -> bytes:
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"{path.name}: corrupt DOCX member {bad_member}")
        names = set(archive.namelist())
        required_parts = {"[Content_Types].xml", "word/document.xml", "docProps/core.xml"}
        missing = required_parts - names
        if missing:
            raise ValueError(f"{path.name}: missing DOCX parts {sorted(missing)}")
        return b"\n".join(
            archive.read(name)
            for name in sorted(names)
            if name.endswith((".xml", ".rels"))
        )


def docx_metrics(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        document = ET.fromstring(archive.read("word/document.xml"))
        core = ET.fromstring(archive.read("docProps/core.xml"))

        paragraphs: list[str] = []
        reference_count = 0
        for paragraph in document.findall(".//w:p", NS):
            text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
            paragraphs.append(text)
            style = paragraph.find("./w:pPr/w:pStyle", NS)
            style_id = style.attrib.get(W + "val", "") if style is not None else ""
            if style_id.lower().replace("_", "") == "bibentry":
                reference_count += 1

        body_text = "\n".join(paragraphs)
        citation_numbers: set[int] = set()
        for group in re.findall(r"\[([0-9, ]+)\]", body_text):
            citation_numbers.update(int(value) for value in re.findall(r"\d+", group))

        sections = document.findall(".//w:sectPr", NS)
        if not sections:
            raise ValueError(f"{path.name}: no section properties")
        section = sections[-1]
        page_size = section.find("w:pgSz", NS)
        margins = section.find("w:pgMar", NS)
        columns = section.find("w:cols", NS)

        creator = core.find("dc:creator", NS)
        subject = core.find("dc:subject", NS)
        last_modified_by = core.find("cp:lastModifiedBy", NS)

        return {
            "tables": len(document.findall(".//w:tbl", NS)),
            "figures": len(document.findall(".//a:blip", NS)),
            "references": reference_count,
            "citations": sorted(citation_numbers),
            "sections": len(sections),
            "page_width_twips": int(page_size.attrib[W + "w"]) if page_size is not None else None,
            "page_height_twips": int(page_size.attrib[W + "h"]) if page_size is not None else None,
            "left_margin_twips": int(margins.attrib[W + "left"]) if margins is not None else None,
            "right_margin_twips": int(margins.attrib[W + "right"]) if margins is not None else None,
            "top_margin_twips": int(margins.attrib[W + "top"]) if margins is not None else None,
            "bottom_margin_twips": int(margins.attrib[W + "bottom"]) if margins is not None else None,
            "columns": int(columns.attrib.get(W + "num", "1")) if columns is not None else 1,
            "creator": creator.text if creator is not None else "",
            "last_modified_by": last_modified_by.text if last_modified_by is not None else "",
            "subject": subject.text if subject is not None else "",
            "tracked_insertions": len(document.findall(".//w:ins", NS)),
            "tracked_deletions": len(document.findall(".//w:del", NS)),
            "highlights": len(document.findall(".//w:highlight", NS)),
            "comment_parts": sorted(name for name in names if "comment" in name.lower()),
        }


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def docx_tables(path: Path) -> list[list[list[str]]]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
    tables: list[list[list[str]]] = []
    for table in document.findall(".//w:tbl", NS):
        rows: list[list[str]] = []
        for row in table.findall("./w:tr", NS):
            cells: list[str] = []
            for cell in row.findall("./w:tc", NS):
                paragraph_text = [
                    "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
                    for paragraph in cell.findall("./w:p", NS)
                ]
                cells.append(normalize_text(" ".join(paragraph_text)))
            rows.append(cells)
        tables.append(rows)
    return tables


def docx_references(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
    references: list[str] = []
    for paragraph in document.findall(".//w:p", NS):
        style = paragraph.find("./w:pPr/w:pStyle", NS)
        style_id = style.attrib.get(W + "val", "") if style is not None else ""
        if style_id.lower().replace("_", "") != "bibentry":
            continue
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
        references.append(normalize_text(text))
    return references


def csv_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return [[normalize_text(value) for value in row] for row in csv.reader(stream)]


def markdown_references(path: Path) -> list[str]:
    references: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\[(\d+)\]\s+(.+)$", line)
        if match:
            references.append(normalize_text(match.group(2).replace("*", "")))
    return references


def pdf_page_markers(path: Path) -> int:
    data = path.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-4096:]:
        raise ValueError(f"{path.name}: invalid PDF signature or EOF")
    return len(re.findall(rb"/Type\s*/Page(?!s)\b", data))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = parse_manifest()
    except Exception as exc:
        print(f"MANIFEST ERROR: {exc}")
        return 1

    actual_files = package_files()
    missing_required = REQUIRED - actual_files
    if missing_required:
        errors.append(f"required files missing: {sorted(missing_required)}")

    manifest_files = set(manifest)
    if manifest_files != actual_files:
        missing_from_manifest = actual_files - manifest_files
        stale_manifest = manifest_files - actual_files
        if missing_from_manifest:
            errors.append(f"files missing from manifest: {sorted(missing_from_manifest)}")
        if stale_manifest:
            errors.append(f"manifest paths not found: {sorted(stale_manifest)}")

    for rel, expected in sorted(manifest.items()):
        path = ROOT / rel
        if not path.is_file():
            continue
        actual = sha256(path)
        if actual != expected:
            errors.append(f"SHA-256 mismatch: {rel}")

    for rel in sorted(actual_files):
        path = ROOT / rel
        size = path.stat().st_size
        if size > 100 * 1024 * 1024:
            errors.append(f"file exceeds 100 MB: {rel} ({size} bytes)")
        elif size > 50 * 1024 * 1024:
            warnings.append(f"file exceeds 50 MB: {rel} ({size} bytes)")

        lower_rel = rel.lower().encode()
        if any(marker in lower_rel for marker in PROJECT_MARKERS):
            errors.append(f"unrelated-project marker in path: {rel}")

        if path.suffix.lower() in TEXT_SUFFIXES:
            data = path.read_bytes()
            lower_data = data.lower()
            if any(marker in lower_data for marker in PROJECT_MARKERS):
                errors.append(f"unrelated-project marker in text: {rel}")
            if any(pattern.search(data) for pattern in SECRET_PATTERNS):
                errors.append(f"credential-like string in text: {rel}")

    for rel in sorted(actual_files):
        if rel.endswith(".docx"):
            try:
                payload = docx_payload(ROOT / rel)
            except Exception as exc:
                errors.append(str(exc))
                continue
            if "Final_Anonymous" in rel:
                for token in IDENTITY_TOKENS:
                    if token.lower() in payload.lower():
                        errors.append(f"anonymous DOCX contains identity token: {token.decode()}")
            if any(pattern.search(payload) for pattern in SECRET_PATTERNS):
                errors.append(f"credential-like string in DOCX package: {rel}")
            if "/final/" in f"/{rel}":
                try:
                    metrics = docx_metrics(ROOT / rel)
                except Exception as exc:
                    errors.append(f"{rel}: structural audit failed: {exc}")
                    continue
                expected_geometry = {
                    "tables": 3,
                    "figures": 2,
                    "references": 20,
                    "citations": list(range(1, 21)),
                    "sections": 1,
                    "page_width_twips": 12240,
                    "page_height_twips": 15840,
                    "left_margin_twips": 1440,
                    "right_margin_twips": 2040,
                    "top_margin_twips": 1760,
                    "bottom_margin_twips": 2840,
                    "columns": 1,
                    "tracked_insertions": 0,
                    "tracked_deletions": 0,
                    "highlights": 0,
                    "comment_parts": [],
                }
                for key, expected in expected_geometry.items():
                    if metrics[key] != expected:
                        errors.append(
                            f"{rel}: {key}={metrics[key]!r}, expected {expected!r}"
                        )
                if "Final_Anonymous" in rel:
                    if metrics["creator"] != "Anonymous" or metrics["last_modified_by"] != "Anonymous":
                        errors.append(f"{rel}: anonymous core identity is not Anonymous")
                    if metrics["subject"] != "AICSS 2026 double-blind submission":
                        errors.append(f"{rel}: unexpected anonymous Subject metadata")
                if "Final_Author_Copy" in rel:
                    if metrics["creator"] != "Lin Zhanyi" or metrics["last_modified_by"] != "Lin Zhanyi":
                        errors.append(f"{rel}: author-copy core identity mismatch")
                    if metrics["subject"] != "AICSS 2026 author copy":
                        errors.append(f"{rel}: unexpected author-copy Subject metadata")

        if rel.endswith(".pdf"):
            try:
                pages = pdf_page_markers(ROOT / rel)
            except Exception as exc:
                errors.append(str(exc))
                continue
            if "/final/" in f"/{rel}" and pages != 8:
                errors.append(f"final PDF page-marker count is {pages}, expected 8: {rel}")
            if "Final_Anonymous" in rel:
                data = (ROOT / rel).read_bytes().lower()
                for token in IDENTITY_TOKENS:
                    if token.lower() in data:
                        errors.append(f"anonymous PDF contains raw identity token: {token.decode()}")

    anonymous_docx = ROOT / "manuscript/final/SongCi_AICSS2026_Final_Anonymous.docx"
    if anonymous_docx.is_file():
        extracted_tables = docx_tables(anonymous_docx)
        table_paths = [
            ROOT / "data/table1_corpus_flow.csv",
            ROOT / "data/table2_candidate_choice_audit.csv",
            ROOT / "data/table3_bounded_cases.csv",
        ]
        if len(extracted_tables) != len(table_paths):
            errors.append(
                f"anonymous DOCX has {len(extracted_tables)} tables, expected {len(table_paths)}"
            )
        else:
            for index, (actual_rows, table_path) in enumerate(
                zip(extracted_tables, table_paths), 1
            ):
                if not table_path.is_file() or actual_rows != csv_rows(table_path):
                    errors.append(f"CSV does not match manuscript table {index}: {table_path.name}")

        extracted_references = docx_references(anonymous_docx)
        reference_path = ROOT / "references/REFERENCES.md"
        if not reference_path.is_file() or extracted_references != markdown_references(reference_path):
            errors.append("REFERENCES.md does not match the anonymous manuscript bibliography")

    print(f"Manifest entries: {len(manifest)}")
    print(f"Package files: {len(actual_files)}")
    print(f"Files above 50 MB: {sum(1 for x in warnings if '50 MB' in x)}")
    print(f"Files above 100 MB: {sum(1 for x in errors if '100 MB' in x)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("PACKAGE VERIFICATION: FAIL")
        return 1
    print("PACKAGE VERIFICATION: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
