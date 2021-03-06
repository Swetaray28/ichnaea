import uuid

from ichnaea.models.api import ApiKey
from ichnaea.tests.factories import ApiKeyFactory


class TestApiKey(object):

    def test_fields(self, session):
        key = uuid.uuid4().hex
        session.add(ApiKey(
            valid_key=key, maxreq=10,
            allow_fallback=True, allow_locate=True, allow_transfer=True,
            fallback_name='test_fallback',
            fallback_url='https://localhost:9/api?key=k',
            fallback_ratelimit=100,
            fallback_ratelimit_interval=60,
            fallback_cache_expire=86400,
        ))
        session.flush()

        result = session.query(ApiKey).get(key)
        assert result.valid_key == key
        assert result.maxreq == 10
        assert result.allow_fallback is True
        assert result.allow_locate is True
        assert result.allow_transfer is True
        assert result.fallback_name == 'test_fallback'
        assert result.fallback_url == 'https://localhost:9/api?key=k'
        assert result.fallback_ratelimit == 100
        assert result.fallback_ratelimit_interval == 60
        assert result.fallback_cache_expire == 86400

    def test_get(self, session):
        key = uuid.uuid4().hex
        session.add(ApiKey(valid_key=key, shortname='foo'))
        session.flush()

        result = ApiKey.get(session, key)
        assert isinstance(result, ApiKey)
        # shortname wasn't loaded at first
        assert 'shortname' not in result.__dict__
        # but is eagerly loaded
        assert result.shortname == 'foo'

    def test_get_miss(self, session):
        result = ApiKey.get(session, 'unknown')
        assert result is None

    def test_allowed(self):
        api_key = ApiKeyFactory.build(allow_locate=True, allow_transfer=True)
        assert api_key.allowed('locate')
        assert api_key.allowed('region')
        assert api_key.allowed('submit')
        assert api_key.allowed('transfer')
        assert api_key.allowed('unknown') is None
        assert not ApiKeyFactory.build(allow_locate=None).allowed('locate')
        assert not ApiKeyFactory.build(allow_locate=False).allowed('locate')
        assert not ApiKeyFactory.build(allow_transfer=None).allowed('transfer')

    def test_can_fallback(self):
        assert ApiKeyFactory.build(allow_fallback=True).can_fallback()
        assert not ApiKeyFactory.build(allow_fallback=False).can_fallback()
        assert not ApiKeyFactory.build(allow_fallback=None).can_fallback()
        assert not (ApiKeyFactory.build(
            allow_fallback=True, fallback_name=None).can_fallback())
        assert not (ApiKeyFactory.build(
            allow_fallback=True, fallback_url=None).can_fallback())
        assert not (ApiKeyFactory.build(
            allow_fallback=True, fallback_ratelimit=None).can_fallback())
        assert (ApiKeyFactory.build(
            allow_fallback=True, fallback_ratelimit=0).can_fallback())
        assert not (ApiKeyFactory.build(
            allow_fallback=True,
            fallback_ratelimit_interval=None).can_fallback())
        assert not (ApiKeyFactory.build(
            allow_fallback=True,
            fallback_ratelimit_interval=0).can_fallback())
        assert (ApiKeyFactory.build(
            allow_fallback=True, fallback_cache_expire=None).can_fallback())
        assert (ApiKeyFactory.build(
            allow_fallback=True, fallback_cache_expire=0).can_fallback())

    def test_str(self):
        assert 'foo' in str(ApiKey(valid_key='foo'))
