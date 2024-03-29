import time
import random
from contextlib import contextmanager

from django.core.cache import cache as default_cache
from django.db import transaction

from viewflow.exceptions import FlowLockFailed


try:
    import django_redis  # NOQA
except ImportError:
    raise ImportError('django-redis required')


class RedisLock(object):
    """
    Task lock based on redis' cache capabilities.

    Example::

        class MyFlow(Flow):
            lock_impl = RedisLock(cache=caches['locks'])

    The example uses a different cache. The default cache
    is Django ``default`` cache configuration.

    ..note::
        This lock requires a ``django-redis`` cache backend.

    """

    def __init__(self, cache=default_cache, attempts=5, expires=120):
        self.cache = cache
        self.attempts = attempts
        self.expires = expires

    def __call__(self, flow):  # noqa D102
        @contextmanager
        def lock(flow_class, process_pk):
            key = 'django-viewflow-lock-{}/{}'.format(flow_class._meta.flow_label, process_pk)

            for i in range(self.attempts):
                lock = self.cache.lock(key, timeout=self.expires)
                if lock.acquire(blocking=False):
                    break
                if i != self.attempts - 1:
                    sleep_time = (((i + 1) * random.random()) + 2 ** i) / 2.5
                    time.sleep(sleep_time)
            else:
                raise FlowLockFailed('Lock failed for {}'.format(flow_class))

            try:
                with transaction.atomic():
                    yield
            finally:
                lock.release()

        return lock


redis_lock = RedisLock()
