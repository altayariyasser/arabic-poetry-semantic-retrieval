"""Run exposed demonstration queries against a running local app, not a benchmark."""
import argparse
import json
import time
from pathlib import Path
from gradio_client import Client

CASES = [
    ('مدح', 'شخص كريم يساعد المحتاجين ويشتهر بحسن الضيافة.'),
    ('هجاء', 'شخص بخيل يعد الناس بالخير ثم يخلف وعده.'),
    ('غزل', 'محب يشتاق إلى حبيبته بعد طول غياب وفراق.'),
    ('فخر', 'شخص يعتز بشجاعته وكرامته ولا يرضى بالذل.'),
    ('رثاء', 'شخص يحزن على وفاة أخيه ويتذكر خصاله الطيبة.'),
    ('عتاب', 'صديق يعاتب صاحبه لأنه هجره ونسي المودة بينهما.'),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:7860')
    parser.add_argument('--output', default='.local-verification/http_smoke.json')
    args = parser.parse_args()
    client = Client(args.url, verbose=False)
    results = []
    for genre, description in CASES:
        start = time.perf_counter()
        markup = client.predict(description, genre, api_name='/retrieve')
        assert markup.count('class="poetry-card"') == 3, genre
        assert 'https://' in markup, genre
        results.append({'genre': genre, 'description': description,
                        'elapsed_seconds': time.perf_counter() - start,
                        'candidate_count': 3, 'html': markup})
        print(f'{genre}: three sourced candidates', flush=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'scope': 'Six exposed development smoke queries; not relevance evaluation',
                                  'cases': results}, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    main()
