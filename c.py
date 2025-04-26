import logging
import os

from dotenv import load_dotenv

load_dotenv()
LANG = os.getenv('EXTRACT_LANG', 'en')

LANG_SUFFIX = '_' + LANG if LANG != 'jp' else ''

logger = logging.getLogger(__file__.rsplit('/')[-1])
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s | %(filename)s:%(lineno)d | %(message)s')
