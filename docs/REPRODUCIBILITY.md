# Reproducibility and Archive Boundary

## Canonical source and render

The two DOCX files in `manuscript/final/` are the editable manuscript sources. Their paired PDFs are frozen renderings produced in the 2026-09-04 document environment. A new export from Word, WPS, or LibreOffice may preserve visible content while changing pagination, font metrics, PDF metadata, or binary hashes.

For the frozen archive, verify the supplied PDFs rather than assuming a fresh export is byte-identical. Each frozen PDF must have eight US Letter pages, one column, three tables, two grayscale figures, and twenty references.

## Integrity check

Run from the repository root:

```powershell
python scripts/verify_package.py
```

The script uses only the Python standard library. It checks every SHA-256 entry, confirms that the manifest covers the package, opens each DOCX as a ZIP archive, checks PDF signatures and page markers, tests the anonymous files for misplaced author identity, scans text/package names for unrelated-project markers and common credential patterns, and reports files above 50 MB and 100 MB.

## Data and references

The source corpus is not vendored. Retrieve the Chinese-Poetry repository at the commit pinned in `docs/METHODS_AND_DATA.md`. The later source witness is identified in reference [8]. The CSV files in `data/` reproduce the three tables in the frozen manuscript with display line breaks normalized to spaces.

`references/REFERENCES.md` contains the twenty frozen bibliography entries. `audit/citation-verification.json` records DOI/API or direct-source resolution captured on 2026-09-03; it is evidence of that check date, not a guarantee that all remote URLs remain available indefinitely.

## Deliberate exclusions

The archive excludes local lock files, temporary builds, page-render QA images, private chat exports, third-party language-source documents, detector reports, local absolute paths, and credentials. These exclusions do not change the four frozen manuscript files or the exact table and reference content.
