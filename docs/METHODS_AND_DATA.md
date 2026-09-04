# Frozen Methods and Data Summary

This file summarizes the method and values already present in the frozen manuscript. It does not add experiments, observations, or interpretations.

## Research objects

The analysis keeps three objects separate:

1. A codification layer from a fixed digital witness of the Siku *Qinding Cipu* (1715), pinned to nine page revisions for ten exact stored tune labels.
2. A textual-realization layer containing modern digital poem records and declared residuals from the selected later pattern.
3. An expression-space layer based on character 1-2-gram TF-IDF followed by truncated SVD.

The arrows between these objects are analytical mappings. They do not assert a causal path from a Qing witness to Song textual practice and do not reconstruct Song-period pronunciation.

## Frozen corpus boundary

The corpus source is the Chinese-Poetry Song Ci repository at commit [`b8594f81a89752241442f2ce267d6f66f96704ee`](https://github.com/chinese-poetry/chinese-poetry/commit/b8594f81a89752241442f2ce267d6f66f96704ee).

| Stage | Records | Boundary |
|---|---:|---|
| Ingested | 21,053 | 21,050 primary plus 3 supplemental records |
| Low-frequency label excluded | 4,570 | Continuity rule, not tune-identity adjudication |
| Lost tune name excluded | 372 | Exact stored-label boundary |
| Continuity layer retained | 16,111 | Records under 99 exact stored labels |
| Ten-label pilot aligned | 5,575 | Purposive pilot across nine source volumes |
| Exact source-exemplar match excluded | 1 | Pre-existing leakage rule |
| Formal pilot retained | 5,574 | Records, not deduplicated independent works |

The ten-label pilot is purposive rather than a probability sample. Huanxisha contributes 776 records. Author strings are dependency blocks, not authenticated historical identities. Rhyme is applicable to 5,534 records, with 5,521 in common support for the baseline candidate audit.

## Representation and estimands

The expression representation uses character 1-2-gram TF-IDF and a frozen 128-dimensional SVD. Outcomes are within-tune author-centroid dispersion and same-tune leave-one-record cosine distance. They measure character-use geometry, not meaning, creativity, style, or literary value.

Eighteen tune-level relationships are prespecified: ten pair source-side properties with two expression-space summaries, and eight pair tune-level realization summaries with those outcomes. At record level, residual predictors and distance outcomes are average-ranked within exact stored labels and standardized. The models include standardized `log1p` record length and tune fixed effects.

Record-level uncertainty uses author-string-clustered 95% confidence intervals and 9,999 author-block sign flips with seed `20260804`. Raw values are Holm-adjusted across eight effects.

## Frozen audits

- **Audit A:** Adds tune-wise mean log text length to all 18 aggregate relationships; uses 99,999 Freedman-Lane residual permutations and 5,000 requested tune-resample bootstrap draws. Passing requires a within-family Holm-adjusted value below .05, an interval excluding zero, and a common sign in all leave-one-tune-out estimates.
- **Audit B:** Retains every candidate tied on the frozen segment and character-span score. It evaluates strict ranking reversals, a pooled reversible-pair proportion, 2,000 requested author-string-block bootstrap repetitions, and frozen 10% high/low sets under three deterministic candidate rules. Sensitivity and stability use the prespecified .05 and .90 audit thresholds.
- **Audit C:** Repeats Audit B under isolated conflict-exclusion, anonymous-label-exclusion, and anonymous-singleton policies.
- **Adverse control:** Compares the prespecified true-tune outcome with a deterministic wrong-tune outcome. The constructions are non-symmetric, so the control warns about specificity but is not a direct coefficient-equality test.

## Frozen findings

- After mean-length adjustment, 0/18 tune-level effects pass the complete joint gate.
- At record level, 0/8 primary estimands are Holm-supported; all eight adjusted values are `q = 1.000`.
- Tone residual under the true-tune construction is `beta = -0.026`, 95% CI `[-0.061, 0.009]`, `q = 1.0000`.
- Tone residual under the wrong-tune construction is `beta = -0.067`, 95% CI `[-0.102, -0.032]`, `q = .0016`.
- No direct `beta_wrong - beta_true` contrast was estimated.
- Baseline candidate-choice tone sensitivity has interval `[0.185797, 0.308446]`, minimum Jaccard `0.209302`, and 12 changed deterministic comparisons.
- Baseline rhyme sensitivity has interval `[0.049921, 0.091889]`, minimum Jaccard `0.175573`, and 6 changed comparisons; it remains indeterminate under the frozen rule.
- Huanxisha contributes 72.2% of the reversible-pair numerator for tone and 91.3% for rhyme; pooled sensitivity is therefore not a typical-tune result.

Exact manuscript tables are stored as CSV files in `data/`.

## Reproduction limits

This repository does not redistribute the external corpus or the pinned source pages. It also does not claim to contain a complete independent rerun environment for every statistical result. The included DOCX files are the editable manuscript sources; the PDFs, table extracts, references, citation audit, method record, and hash manifest reproduce and verify the frozen paper package. A full analytical rerun additionally requires retrieving the pinned external sources and the original analysis implementation under their applicable terms.
