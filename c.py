import logging
import os

from dotenv import load_dotenv

# only used by extraction code, not relevant for other uses, may be refactored later
load_dotenv()
LANG = os.getenv('EXTRACT_LANG', 'en')

LANG_SUFFIX = ('_' + LANG) if LANG != 'jp' else '_ja'
LANG_SUFFIX_1 = ('_' + LANG) if LANG != 'jp' else ''
SEP = '|' if LANG == 'en' else ','
SUPPORTED_LANGS = ('en', 'jp')

logger = logging.getLogger(__file__.rsplit('/')[-1])
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(filename)s:%(lineno)d | %(message)s')
