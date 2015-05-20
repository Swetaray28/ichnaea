from ichnaea.config import DummyConfig
from ichnaea.tests.base import (
    _make_app,
    _make_db,
    DBTestCase,
    RedisIsolation,
    REDIS_URI,
    SQLURI,
)


class TestApp(RedisIsolation, DBTestCase):

    def test_db_hooks(self):
        app_config = DummyConfig({'ichnaea': {
            'db_master': SQLURI,
            'db_slave': SQLURI,
        }})
        app = _make_app(app_config=app_config,
                        _raven_client=self.raven_client,
                        _redis_client=self.redis_client,
                        _stats_client=self.stats_client,
                        )
        self.db_rw = app.app.registry.db_rw
        self.db_ro = app.app.registry.db_ro
        app.get('/stats_wifi.json', status=200)

    def test_db_config(self):
        self.db_rw = _make_db()
        self.db_ro = _make_db()
        app = _make_app(_db_rw=self.db_rw,
                        _db_ro=self.db_ro,
                        _raven_client=self.raven_client,
                        _redis_client=self.redis_client,
                        _stats_client=self.stats_client,
                        )
        app.get('/stats_wifi.json', status=200)

    def test_redis_config(self):
        app_config = DummyConfig({'ichnaea': {
            'db_master': SQLURI,
            'db_slave': SQLURI,
            'redis_url': REDIS_URI,
        }})
        app = _make_app(app_config=app_config,
                        _raven_client=self.raven_client,
                        _stats_client=self.stats_client)
        self.assertTrue(app.app.registry.redis_client is not None)
