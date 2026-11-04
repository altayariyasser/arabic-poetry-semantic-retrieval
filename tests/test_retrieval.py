"""Offline mechanics checks with synthetic fixtures, never the final-test split."""
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
import numpy as np
from src.lexical import BM25, normalize
from src.engine import FinalEngine, input_conflict
from src.rendering import render


class RetrievalTests(unittest.TestCase):
    def test_arabic_normalization_preserves_negation(self):
        self.assertEqual(normalize('لَا يَكْذِبُ ـ'), 'لا يكذب')
        self.assertNotEqual(normalize('لا يكذب'), normalize('يكذب'))

    def test_bm25_rare_word_and_unknown_query(self):
        bm = BM25(['كرم عطاء', 'شوق حب', 'عطاء'])
        scores = bm.score('كرم')
        self.assertGreater(scores[0], scores[1])
        self.assertEqual(bm.score('غيرموجود'), [0., 0., 0.])

    def test_input_consistency_check(self):
        self.assertEqual(input_conflict('أخي على قيد الحياة', 'رثاء'), 'living_person_elegy_conflict')
        self.assertIsNone(input_conflict('أخي على قيد الحياة', 'مدح'))
        self.assertIsNone(input_conflict('أخي توفي', 'رثاء'))

    def fixture(self):
        engine = FinalEngine.__new__(FinalEngine)
        engine.rows = [
            {'pair_id': 'b', 'genre': 'مدح', 'bayt': 'كرم'},
            {'pair_id': 'a', 'genre': 'مدح', 'bayt': 'كَرَم'},
            {'pair_id': 'c', 'genre': 'غزل', 'bayt': 'حب'},
            {'pair_id': 'd', 'genre': 'مدح', 'bayt': 'عطاء'},
        ]
        engine.vectors = np.array([[1., 0.], [1., 0.], [1., 0.], [0., 1.]])
        engine.verse_vectors = engine.vectors.copy()
        engine.bm25 = BM25([r['bayt'] for r in engine.rows])
        engine.encoder = Mock()
        engine.encoder.encode.return_value = np.array([[1., 0.]])
        engine.encoder.tokenizer.encode.return_value = [1, 2]
        engine.cache = {}
        return engine

    def test_filter_tie_break_dedup_rrf_and_cache(self):
        engine = self.fixture()
        result = engine.rankings('كرم', 'مدح')
        self.assertEqual([m['record']['pair_id'] for m in result['e5_description']], ['a', 'd'])
        self.assertEqual(result['hybrid'][0]['record']['pair_id'], 'a')
        self.assertAlmostEqual(result['hybrid'][0]['rrf'], 2 / 61)
        self.assertTrue(all(m['record']['genre'] == 'مدح' for v in result.values() for m in v))
        engine.rankings('كرم', 'غزل')
        engine.encoder.encode.assert_called_once_with(['query: كرم'])

    def test_invalid_and_too_long_inputs(self):
        engine = self.fixture()
        self.assertEqual(engine.search('', 'مدح')['status'], 'clarification')
        self.assertEqual(engine.search('كرم', 'invalid')['status'], 'clarification')
        engine.encoder.tokenizer.encode.return_value = [0] * 513
        self.assertEqual(engine.search('كرم', 'مدح')['status'], 'too_long')
        engine.encoder.encode.assert_not_called()

    def test_render_escapes_untrusted_record_text_and_url(self):
        row = dict(pair_id='fixture', genre='مدح', hemistich_1='<script>x</script>',
                   hemistich_2='نص اختباري', poet='<b>name</b>', biography='<img>',
                   source_url='javascript:alert(1)')
        markup = render({'status': 'uncalibrated_candidates', 'matches': [{'record': row, 'cosine': .8}]})
        self.assertNotIn('<script>', markup)
        self.assertNotIn('javascript:', markup)
        self.assertIn('&lt;script&gt;', markup)


if __name__ == '__main__':
    unittest.main()
