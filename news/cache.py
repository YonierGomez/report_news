import time
import logging

logger = logging.getLogger('report_news')

_cache = {}
DEFAULT_TTL = 900  # 15 minutos


def get(key, ttl=DEFAULT_TTL):
    """Retorna datos cacheados si no han expirado, None si no hay o expiró."""
    if key in _cache:
        data, timestamp = _cache[key]
        if time.time() - timestamp < ttl:
            logger.info(f'Cache HIT: {key}')
            return data
        else:
            del _cache[key]
            logger.info(f'Cache EXPIRED: {key}')
    return None


def set(key, data):
    """Guarda datos en caché con timestamp actual."""
    _cache[key] = (data, time.time())
    logger.info(f'Cache SET: {key} ({len(data)} items)')


def clear():
    """Limpia todo el caché."""
    _cache.clear()
    logger.info('Cache CLEARED')
