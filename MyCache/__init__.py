import logging
import redis
from threading import RLock
from django.core.cache import caches
from django.core.cache.backends.base import BaseCache

from mysite.settings import CACHE_SERVERS
from mydemo.models import Reporter, Article


def genarate_key(key, key_prefix='blog', version=1):
    return ':'.join([key_prefix, str(version), key])


class CacheItemBase(object):
    def __init__(self, id):
        self.id = id
        self.name = None


class ReporterCache(CacheItemBase):
    def __init__(self, id):
        self.articles = []
        super(ReporterCache, self).__init__(id)


class ArticlerCache(CacheItemBase):
    def __init__(self, id):
        super(ArticlerCache, self).__init__(id)


class RedisCache(object):
    # Setting Redis Server directly
    POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
    _rc = redis.Redis(connection_pool=POOL)
    _lock = RLock()

    # Setting redis cache using django settings.
    _rc = caches['default']

    @staticmethod
    def get(key):
        logging.info('RedisCache.get({})'.format(key))
        key = genarate_key(key)
        RedisCache._lock.acquire()
        obj = RedisCache._rc.get(key)
        RedisCache._lock.release()
        return obj

    @staticmethod
    def set(key, item):
        logging.info('RedisCache.set({})'.format(key))
        key = genarate_key(key)
        RedisCache._lock.acquire()
        obj = RedisCache._rc.set(key, item)
        RedisCache._lock.release()
        return obj

    @staticmethod
    def delete(key):
        logging.info('RedisCache.delete({})'.format(key))
        key = genarate_key(key)
        RedisCache._lock.acquire()
        obj = RedisCache._rc.delete(key)
        RedisCache._lock.release()
        return obj

    @staticmethod
    def hydrate_reporter_cahce(reporter_id):
        logging.info('RedisCache.hydrate_reporter_cahce({})'.format(reporter_id))

        reporter = Reporter.objects.get(id=reporter_id)
        reporter_cache_item = ReporterCache(reporter_id)
        reporter_cache_item.name = '{} {}'.format(reporter.first_name, reporter.last_name)

        articles = Article.objects.filter(reporter_id=reporter_id)
        for article in articles:
            article_item = RedisCache.hydrate_article_cahce(reporter_id, article.id)
            article_key = {article_item.id: reporter_cache_item.name}
            reporter_cache_item.articles.append(article_key)

        RedisCache.set(reporter_id, reporter_cache_item)
        return reporter_cache_item

    @staticmethod
    def hydrate_article_cahce(reporter_id, id):
        logging.info('RedisCache.hydrate_article_cahce({})'.format(reporter_id, id))

        article = Article.objects.get(id=id)
        article_cache_item = ArticlerCache(reporter_id)
        article_cache_item.name = article.headline

        RedisCache.set(reporter_id, article_cache_item)
        return article_cache_item

