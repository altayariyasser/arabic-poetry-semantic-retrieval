# External pretrained indexes

Two float32 NumPy matrices, `description.npy` and `verse.npy`, each have shape (3000, 384), with L2-normalized rows. `metadata.json` links the byte-exact corpus checksum and row IDs. Existing indexes use pretrained `intfloat/multilingual-e5-small`, revision `614241f622f53c4eeff9890bdc4f31cfecc418b3`, `passage: ` prefix, attention-mask mean pooling and L2 normalization. Queries use `query: `. No poetry fine-tuning occurred.

Provide these files through the authorized external bundle described in ../data/README.md. They are not distributed here. BM25 postings are rebuilt in memory from the existing verses at startup.
