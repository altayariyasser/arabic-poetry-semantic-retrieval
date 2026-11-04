# Hugging Face Spaces deployment

Status: not deployed. No Hugging Face credential was available during preparation. Corpus and embedding redistribution rights remain unresolved. Do not upload the existing corpus, embeddings or poetry-bearing screenshots until cleared. Account billing/hardware availability also needs confirmation; no paid resources were requested.

After resolving those conditions, copy the YAML front matter from `SPACE_README.md` to the Space root README, deploy this app and pinned requirements, securely provide an authorized artifact bundle, and set `ARABIC_POETRY_ARTIFACTS` and `ARABIC_POETRY_E5_PATH`. The model must already be present at the pinned revision; the application is offline by default. Launch with `python app.py --host 0.0.0.0 --port 7860` (or set `GRADIO_SERVER_NAME=0.0.0.0`). The native Gradio Space runner uses its own binding configuration. Test all six genres and source links before adding a live URL.

Official reference: https://huggingface.co/docs/hub/spaces-sdks-gradio
