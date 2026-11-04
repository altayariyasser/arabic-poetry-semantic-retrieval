# Dataset access and provenance

The existing local project has 3,000 records: 500 each for مدح، هجاء، غزل، فخر، رثاء، عتاب; 590 recorded poet strings and 2,998 poem families. The original corpus SHA-256 is `e1c087396c21ad5c213475480e7b286cfcafaa05b18815e58d8f4311d8bf1f85`.

Origin: [arbml/ashaar](https://huggingface.co/datasets/arbml/ashaar). The historical local audit inspected 254,630 poems in two Parquet shards. The selected records retain source URLs, poem IDs, poet attribution, original text and automated descriptions. A poet biography does not establish the subject of a verse. 2,990 descriptions originated from automated lexical templates; ten from an individually approved pilot. Bulk semantic approval is separate from independent source verification and permission to redistribute or train.

Corpus, split files and derived embeddings are deliberately excluded from Git. Rights remain unresolved; downloading the upstream dataset does not reproduce or clear this selected bundle. No automated acquisition or new dataset finalization is performed by this release.

To run with an already authorized bundle, set `ARABIC_POETRY_ARTIFACTS` to a directory containing `data/original_records.jsonl`, `indexes/metadata.json`, `indexes/description.npy`, and `indexes/verse.npy`. Preserve the original split ledger. The app searches the existing whole corpus; demo queries are exposed development checks, not untouched final-test evaluation.

Minimum record fields used by the app: `pair_id`, `genre`, `bayt`, `hemistich_1`, `hemistich_2`, `biography`, `poet`, `source_url`. Existing provenance/review fields must remain intact. Index metadata must contain the corpus `source_sha256` and `ordered_ids` in matrix order.
