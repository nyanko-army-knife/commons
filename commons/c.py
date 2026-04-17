import logging
import os

from dotenv import load_dotenv

# only used by extraction code, not relevant for other uses, may be refactored later
load_dotenv()
LANG = os.getenv('EXTRACT_LANG', 'en')

match LANG:
	case 'en':
		SEP = '|'
		LANG_SUFFIX = '_en'
		LANG_SUFFIX_1 = '_en'
	case 'kr':
		SEP = '|'
		LANG_SUFFIX = '_ko'
		LANG_SUFFIX_1 = '_ko'
	case 'tw':
		SEP = '|'
		LANG_SUFFIX = '_tw'
		LANG_SUFFIX_1 = '_tw'
	case 'jp':
		SEP = ','
		LANG_SUFFIX = '_ja'
		LANG_SUFFIX_1 = ''
SUPPORTED_LANGS = ('en', 'jp', 'kr', 'tw')

logger = logging.getLogger(__file__.rsplit('/')[-1])
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(filename)s:%(lineno)d | %(message)s')
