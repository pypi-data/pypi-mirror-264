# import the logging library
import logging

from django.core.cache import cache

# Create a logger for this file
# Get an instance of a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def remove_cache_by_key(key_name):  
    logger.info(f'starting to remove all cache.') 
    for key in cache.keys(key_name):
        logger.info(f'completed remove {key} cache.')
        [cache.delete(i) for i in cache.get(key, [])]
        cache.delete(key)
    logger.info(f'completed remove all cache.')
