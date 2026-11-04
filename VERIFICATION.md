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

Remaining: browser capture host unavailable, so no real screenshot/GIF was captured; invalid saved GitHub CLI login blocks upload and rendered README verification. The local commit uses the requested GitHub username and its privacy-preserving `altayariyasser@users.noreply.github.com` author address, without changing global Git identity. Hugging Face deployment was not performed: credentials were absent and corpus/index rights remain unresolved. No repository URL or live-demo URL has been verified.
