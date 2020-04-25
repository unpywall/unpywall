import pytest
import os
import time
from requests import Response
from shutil import copyfile

from unpywall.cache import UnpywallCache
from unpywall.utils import UnpywallCredentials


class TestUnpywallCache:

    test_dir = os.path.abspath(os.path.dirname(__file__))

    @pytest.fixture
    def example_cache(self):

        UnpywallCredentials('bganglia892@gmail.com')

        copyfile(os.path.join(TestUnpywallCache.test_dir, 'example_cache'),
                 os.path.join(TestUnpywallCache.test_dir, 'test_cache'))
        cache = UnpywallCache(os.path.join(TestUnpywallCache.test_dir,
                                           'test_cache'))
        assert cache.content != {}
        assert cache.access_times != {}
        return cache

    def test_reset_cache(self, example_cache):
        example_cache.reset_cache()
        assert example_cache.content == {}
        assert example_cache.access_times == {}

    def test_delete(self, example_cache):
        doi = '10.1016/j.jns.2020.116832'
        example_cache.delete(doi)
        assert doi not in example_cache.content
        assert doi not in example_cache.access_times

    def test_timeout(self, example_cache):
        timeout = 1
        doi = '10.1016/j.jns.2020.116832'
        example_cache.timeout = timeout
        assert doi not in example_cache.content
        example_cache.get(doi)
        time.sleep(timeout)
        assert example_cache.timed_out(doi)

    def test_get(self, example_cache):
        doi = '10.1016/j.jns.2020.116832'
        assert doi not in example_cache.content
        assert doi not in example_cache.access_times
        assert isinstance(example_cache.get(doi), Response)

    def test_save_load(self, example_cache):
        doi = '10.1016/j.jns.2020.116832'
        assert doi not in example_cache.content
        assert doi not in example_cache.access_times
        example_cache.get(doi)
        saved_cache_name = str(time.time())
        example_cache.save(saved_cache_name)
        UnpywallCache(saved_cache_name)
        os.remove(saved_cache_name)
        assert doi in example_cache.content
        assert doi in example_cache.access_times

    def test_download(self, example_cache):
        doi = '10.1016/j.jns.2020.116832'
        assert isinstance(example_cache.download(doi, 'raise'), Response)
