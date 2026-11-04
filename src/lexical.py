import collections,math,re,unicodedata

GENRES = ('مدح', 'هجاء', 'غزل', 'فخر', 'رثاء', 'عتاب')

def normalize(s, fold=False):
    s = ''.join((c for c in unicodedata.normalize('NFC', s) if unicodedata.category(c) != 'Mn' and c != 'ـ'))
    if fold:
        s = s.translate(str.maketrans('أإآٱى', 'ااااي'))
    return ' '.join(re.findall('[\\w]+', s))

def tokens(s, fold=False):
    return normalize(s, fold).split()

class BM25:

    def __init__(self, texts, fold=False, k1=1.2, b=0.75):
        self.fold, self.k1, self.b = (fold, k1, b)
        self.docs = [collections.Counter(tokens(x, fold)) for x in texts]
        self.lengths = [sum(x.values()) for x in self.docs]
        self.avg = sum(self.lengths) / max(1, len(texts))
        self.df = collections.Counter((t for d in self.docs for t in d))
        self.postings = collections.defaultdict(list)
        for i, d in enumerate(self.docs):
            for token, frequency in d.items():
                self.postings[token].append((i, frequency))

    def score(self, query):
        result = [0.0] * len(self.docs)
        N = len(self.docs)
        for t in sorted(set(tokens(query, self.fold))):
            idf = math.log(1 + (N - self.df[t] + 0.5) / (self.df[t] + 0.5))
            for i, f in self.postings[t]:
                result[i] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lengths[i] / max(self.avg, 1)))
        return result
