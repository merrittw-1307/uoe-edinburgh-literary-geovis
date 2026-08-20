# Processed survey data — 20 August 2026

**Source**: `../raw/qualtrics_export_2026-08-20.csv` (16 raw responses, exported from Qualtrics 20 August 2026, 09:42).

**Excluded (3 responses)**, per the data-quality criteria set out in the Study Procedure section of the dissertation:

| Response ID | Reason |
|---|---|
| `R_8s0sOmLq01nwKZj` | Completed in 550s (~9 minutes) against a 50–65 minute target; free-text answers were near-empty ("." / "peak value") throughout. |
| `R_13whaLBm7L7AFW9` | Free-text answers were single letters or near-random ("a" / "b" / "c" / "no" / "en") on required fields, inconsistent with genuine engagement. |
| `R_8TwtlKiJ4GDTfa1` | Completed in 375s (~6 minutes); free-text answers were nonsensical ("Dm" / "Funk" / "Duck" / "Gum") rather than task-relevant. |

**Kept**: 13 responses, split by self-described background (Q-B3) into:
- **Expert** (n=4): background = Literary studies/English literature, Digital humanities, or Information visualisation/HCI/Computer Science
- **General public** (n=9): all other backgrounds

**Translation**: free-text answers originally given in Chinese are preserved verbatim with an inline `[EN translation: ...]` annotation appended by the researcher, rather than being replaced, so the original wording remains auditable.

`survey_cleaned_translated_2026-08-20.csv` is the resulting cleaned dataset used for all analysis in Chapter 5 (Evaluation).

**⚠️ Not tracked in git.** Both `../raw/qualtrics_export_2026-08-20.csv` and `survey_cleaned_translated_2026-08-20.csv` are excluded via `.gitignore` and exist only on this machine, even though the email column has been redacted (`[redacted]`) in both. With a personal-network-recruited sample this small, individual free-text answers and background descriptions carry a real re-identification risk that goes beyond what the PIS's "anonymised" commitment was scoped to cover for a public GitHub repository specifically (as opposed to an academic publication reporting aggregates). Only `metrics_output_2026-08-20.txt` (aggregate counts/percentages only, no per-response identifiers) and `../py/compute_metrics.py` (the analysis script, for reproducibility of the numbers reported in the dissertation) are committed.
