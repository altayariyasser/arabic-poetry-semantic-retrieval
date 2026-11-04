import os
import collections,hashlib,json,re,time
from pathlib import Path
import numpy as np
from .embedding import E5
from .lexical import BM25,GENRES,normalize
HERE=BASE=Path(os.environ.get('ARABIC_POETRY_ARTIFACTS', Path(__file__).resolve().parents[1]))

def input_conflict(bio, genre):
    """Conservative input consistency check, not entailment or candidate validation."""
    if genre != 'رثاء':
        return None
    q = normalize(bio, True)
    alive = bool(re.search('\\b(?:حي|حية)\\b|علي قيد الحياة|لم يمت|لم تمت|ما زال حيا|لا يزال حيا|يتصل بي|تتصل بي|يكلمني كل يوم', q))
    death = bool(re.search('\\b(?:مات|ماتت|توفي|توفيت|استشهد|استشهدت|المرحوم|المرحومة|المتوفي|المتوفاة)\\b', q))
    if alive and (not death):
        return 'living_person_elegy_conflict'
    return None

class FinalEngine:

    def __init__(self):
        corpus = HERE / 'data/original_records.jsonl'
        if not corpus.is_file():
            raise FileNotFoundError('Authorized corpus/index bundle required. See data/README.md and set ARABIC_POETRY_ARTIFACTS.')
        raw = corpus.read_bytes()
        self.rows = [json.loads(s) for s in raw.decode('utf-8').splitlines()]
        self.meta = json.loads((HERE / 'indexes/metadata.json').read_text(encoding='utf-8'))
        assert hashlib.sha256(raw).hexdigest() == self.meta['source_sha256']
        assert [r['pair_id'] for r in self.rows] == self.meta['ordered_ids']
        self.vectors = np.load(HERE / 'indexes/description.npy', allow_pickle=False)
        assert self.vectors.shape == (3000, 384) and np.isfinite(self.vectors).all()
        self.bm25 = BM25([r['bayt'] for r in self.rows])
        self.encoder = E5()
        self.cache = {}
        self.verse_vectors = np.load(BASE / 'indexes/verse.npy', allow_pickle=False)

    def rankings(self, bio, genre):
        if bio not in self.cache:
            if len(self.cache) >= 128:
                self.cache.clear()
            self.cache[bio] = self.encoder.encode(['query: ' + bio])[0]
        v = self.cache[bio]
        eligible = [i for i, r in enumerate(self.rows) if r['genre'] == genre]
        desc = self.vectors @ v
        verse = self.verse_vectors @ v
        lex = self.bm25.score(bio)
        scores = {'bm25_verse': lex, 'e5_verse': verse, 'e5_description': desc}
        orders = {m: sorted(eligible, key=lambda i: (-s[i], self.rows[i]['pair_id'])) for m, s in scores.items()}
        rrf = collections.defaultdict(float)
        for m in ['bm25_verse', 'e5_description']:
            for rank, i in enumerate(orders[m][:100]):
                rrf[i] += 1 / (61 + rank)
        orders['hybrid'] = sorted(rrf, key=lambda i: (-rrf[i], self.rows[i]['pair_id']))

        def items(order):
            out = []
            seen = set()
            for i in order:
                r = self.rows[i]
                key = normalize(r['bayt'])
                if key in seen:
                    continue
                seen.add(key)
                out.append({'record': r, 'cosine': float(desc[i]), 'verse_cosine': float(verse[i]), 'bm25': float(lex[i]), 'rrf': float(rrf.get(i, 0))})
                if len(out) == 3:
                    break
            return out
        return {m: items(o) for m, o in orders.items()}

    def search(self, bio, genre):
        t = time.perf_counter()
        if not bio or not bio.strip() or genre not in GENRES:
            return {'status': 'clarification', 'matches': [], 'comparison': {}}
        if len(self.encoder.tokenizer.encode('query: ' + bio)) > 512:
            return {'status': 'too_long', 'matches': [], 'comparison': {}}
        conflict = input_conflict(bio, genre)
        if conflict:
            return {'status': 'input_conflict', 'reason': conflict, 'matches': [], 'comparison': {}}
        orders = self.rankings(bio, genre)
        return {'status': 'uncalibrated_candidates', 'matches': orders['e5_description'], 'comparison': orders, 'latency_seconds': time.perf_counter() - t, 'selected': 'e5_description', 'acceptance': 'not calibrated'}
