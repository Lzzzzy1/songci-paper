# Song Ci AICSS 2026 Manuscript Archive

This private repository is the frozen manuscript archive for **Retrospective Prosodic Codification and Analytical Visibility in Song Ci: A Leakage- and Uncertainty-Audited Computational-Linguistic Study**.

**Freeze date:** 2026-09-04
**Archive status:** manuscript package only. This repository is not evidence of conference submission, acceptance, publication, or indexing.

## Canonical manuscript files

Use the anonymous version for a double-blind review system unless the venue explicitly asks for author identity.

| Purpose | Editable source | Frozen PDF |
|---|---|---|
| Double-blind submission | `manuscript/final/SongCi_AICSS2026_Final_Anonymous.docx` | `manuscript/final/SongCi_AICSS2026_Final_Anonymous.pdf` |
| Author backup | `manuscript/final/SongCi_AICSS2026_Final_Author_Copy.docx` | `manuscript/final/SongCi_AICSS2026_Final_Author_Copy.pdf` |

Both frozen PDFs contain eight US Letter pages in a single-column layout. Each version contains three tables, two grayscale figures, and twenty numbered references.

## Repository map

- `manuscript/final/` — current anonymous and author DOCX/PDF files.
- `data/` — exact table values extracted from the frozen manuscript, with line-break whitespace normalized for CSV.
- `references/REFERENCES.md` — the twenty references retained in the manuscript.
- `docs/METHODS_AND_DATA.md` — frozen corpus, representation, audit, result, and limitation summary.
- `docs/REPRODUCIBILITY.md` — manuscript reproduction and verification boundary.
- `audit/INTERNAL_QA.md` and `audit/INTERNAL_QA.json` — neutral internal quality record.
- `audit/citation-verification.json` — citation-resolution evidence captured on 2026-09-03.
- `MANIFEST.sha256` — SHA-256 inventory for every tracked package file except the manifest itself.
- `.gitattributes` — preserves LF text bytes and treats DOCX/PDF files as binary.
- `scripts/verify_package.py` — dependency-free integrity, privacy-placement, project-isolation, and size checks.

## Verify the package

From the repository root, run:

```powershell
python scripts/verify_package.py
```

A successful run ends with `PACKAGE VERIFICATION: PASS`. The script verifies the manifest, required files, DOCX ZIP integrity, PDF signatures and page markers, anonymous-file identity isolation, repository scope, and 50/100 MB thresholds.

## Research scope

The study treats a frozen digital witness of the Qing *Qinding Cipu* as a retrospective knowledge model, not as a direct reconstruction of Song pronunciation or authorial practice. It keeps later codification, recorded textual realization, and character-use expression space separate. The frozen corpus contains 21,053 records; the continuity layer retains 16,111 records under 99 exact stored tune labels; and the ten-label formal pilot retains 5,574 records after one exact source-exemplar match is excluded.

The primary claims remain deliberately limited: 0/18 tune-level effects pass the length-adjusted joint gate and 0/8 primary record-level estimands are Holm-supported. Candidate-pattern and metadata-policy sensitivity is reported as an audit of analytical visibility, not as a performance improvement or universal historical law.

## Legacy snapshot

`manuscript/SongCi_unified_current.docx` and `.pdf` are an earlier repository snapshot preserved to retain the existing Git history. They are not the current submission files. The four files under `manuscript/final/` are authoritative for this freeze.
