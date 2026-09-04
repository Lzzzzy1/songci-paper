# Internal Quality Record

**Freeze:** 2026-09-04
**Scope:** the four files under `manuscript/final/` and their private archival package.

This record is an internal integrity and presentation audit. It is not proof of submission, acceptance, publication, or indexing.

## Frozen file identity

| File | Bytes | SHA-256 |
|---|---:|---|
| `SongCi_AICSS2026_Final_Anonymous.docx` | 193,412 | `CC490CF82FE2601397238F190888E1C6F98371C02BDC23B4196FD7A9578FEDF9` |
| `SongCi_AICSS2026_Final_Anonymous.pdf` | 489,665 | `A882DB4A3C220A033E759CFF308CE0D4998DA2568B330883995B8E7204FA6A09` |
| `SongCi_AICSS2026_Final_Author_Copy.docx` | 193,473 | `E184D74719DE83F04AD5D4A8CB592E95FE29CC3C888EF0805F64CBD38B371BF1` |
| `SongCi_AICSS2026_Final_Author_Copy.pdf` | 490,738 | `6C0AD7DBD3A1BA198657DECFFBC3A0CB65E807F9A217F2AD1BAA3AA374AD8527` |

The four repository copies match the frozen delivery files byte for byte.

## Document structure

- Both PDFs: 8 pages, US Letter (`612 x 792` points), unencrypted, no form, no JavaScript, no suspect flag.
- Both DOCX files: one section, US Letter (`12240 x 15840` twips), one column.
- Margins: left `1440`, right `2040`, top `1760`, bottom `2840` twips.
- Each version: 3 tables, 2 embedded figures, 20 bibliography entries, and body-citation coverage `[1]` through `[20]`.
- The 31 frozen manuscript values are present in both PDF versions.
- DOCX package checks found no comments, tracked insertions, tracked deletions, or highlights.
- Prior full-page rendering inspected all 16 pages. It found 0 clipping, 0 overlap, 0 blank pages, 0 broken tables, 0 missing glyphs, 0 blue pixels, and 0 strictly non-grayscale pixels.
- Page 5 contains a large lower whitespace area because the next figure and table remain intact on page 6; it is not a blank or missing page.

## Identity placement

- Anonymous DOCX core author and last-modified-by values are `Anonymous`; its Subject is `AICSS 2026 double-blind submission`.
- Anonymous DOCX package and anonymous PDF raw scan contain none of the frozen author name, institution, email local part, or email-domain markers.
- Author-copy DOCX core identity is `Lin Zhanyi`; its Subject is `AICSS 2026 author copy`.
- Anonymous and author files are kept under distinct final filenames and are identified separately in the root README.

## Evidence preservation

- The three CSV files reproduce the three manuscript tables with display-only line breaks normalized to spaces.
- `references/REFERENCES.md` contains 20 consecutively numbered bibliography entries.
- `audit/citation-verification.json` preserves the citation-resolution check captured on 2026-09-03.
- `docs/METHODS_AND_DATA.md` records the pinned corpus commit, frozen sample boundaries, estimands, audit rules, central findings, and interpretation limits without adding results.

## Package safety checks

The repository verifier checks manifest coverage and hashes, required files, DOCX ZIP integrity, final-PDF page markers, anonymous identity isolation, unrelated-project contamination, common credential patterns, and the 50 MB/100 MB thresholds. The committed state is acceptable only when `python scripts/verify_package.py` ends with `PACKAGE VERIFICATION: PASS`.

The frozen local package completed this verification with `PACKAGE VERIFICATION: PASS`, 0 files above 50 MB, and 0 files above 100 MB. The verification is repeated after the final manifest is written and again after the commit.

The package deliberately excludes local lock files, QA page images, temporary builds, chat exports, third-party language-source files, detector reports, machine-specific absolute paths, and credentials.

## Boundaries

The archive verifies the frozen manuscript package. It does not claim an independent replication of the complete analysis, historical-phonology reconstruction, causal identification, or conference outcome.
