import logging,re
from .theme import make_theme
from .rendering import render,notice,EMPTY,LOADING
from .engine import FinalEngine,GENRES
LOG=logging.getLogger(__name__)

class Responder:

    def __init__(self, engine):
        self.engine = engine

    def __call__(self, bio, genre):
        if bio and bio.strip() and (not re.search('[\\u0621-\\u064a]', bio)):
            return render({'status': 'invalid_language'})
        try:
            return render(self.engine.search(bio, genre))
        except Exception:
            LOG.exception('Local retrieval failed')
            return render({'status': 'error'})
