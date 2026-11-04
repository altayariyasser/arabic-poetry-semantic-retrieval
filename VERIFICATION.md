# Executed release checks

Verified locally on 2026-11-04 using the existing project `.venv`, original authorized local bundle and cached pretrained E5 snapshot. The original project files were preserved.

- Six offline unit tests passed: Arabic normalization/negation, lexical matching, input consistency, genre filtering, deterministic ties/deduplication/RRF/cache behavior, token limit handling and HTML escaping (some tests cover several checks).
- Started the standalone `app.py` on a separate local port and received HTTP 200 for Gradio configuration.
- Executed one real exposed description per genre through `/retrieve`; all six returned three candidates with source links. This is an operational smoke check, not a relevance score.
- Recomputed all five methods' saved pooled evaluation metrics and matched the existing metrics to 1e-12. No final-test assessment or new relevance judgments were performed.
- Compared Python ASTs against the existing standalone delivery: E5 encoder, BM25, normalization, ranking, search, input conflict, responder and rendering implementations are unchanged. Original CSS and motion JS checksums match. Release changes adapt imports, artifact paths, launch host/port and missing-data guidance.
- Pinned dependencies were already installed. `pip install --dry-run --no-index -r requirements.txt` and `pip check` passed. Fresh-environment installation and installation from a GitHub clone remain unverified.
- Checked the first source URL from each genre: one source page was readable through the web tool; five returned HTTP 403. Those five cannot be claimed verified. Attribution and source context are not newly certified.

Local raw retrieval responses and source-link inventory are in the ignored `.local-verification/` directory. No poetry text or embedding matrices are included in this Git release.

## Publication follow-up — 2026-11-04

- Reused both prepared commits through a Git bundle in a separate workspace checkout. The original research project and prepared repository were not modified.
- Reran all six unit tests successfully and reproduced all five saved metric aggregates to the existing 1e-12 tolerance.
- Started this checkout's real Gradio app on localhost port 7863 with the original authorized external artifacts and pinned cached E5 snapshot. Repeated all six HTTP smoke queries: each returned three sourced candidates. This is an operational check, not final-test evaluation.
- GitHub CLI authentication succeeded as `altayariyasser` outside the restricted execution sandbox. The earlier invalid-login warning was not proof of invalid credentials; normal sandbox network access failed with WinError 10013.
- Confirmed the requested remote repository did not exist before creating it privately. Corpus/index rights remain unresolved, so those files and poetry-bearing screenshots remain excluded, including from private uploads. No license was added.
- Real screenshot capture failed with `foreground window did not report a process id`; the Chrome connector was unavailable. README includes later capture instructions. No fake screenshot was made.
- README now records one real response using poet names, source references and actual scores while withholding corpus verse text. Raw HTML responses stay in ignored `.local-verification/`.

Push success and final remote commit verification are reported separately in the publication report after execution. No hosted demo or fresh-environment installation is claimed.
