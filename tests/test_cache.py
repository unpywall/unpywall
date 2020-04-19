import pytest
import os
import time
test_dir = os.path.abspath(os.path.dirname(__file__))

from unpywall.cache import UnpywallCache
from unpywall.utils import UnpywallCredentials
from requests.exceptions import HTTPError
from shutil import copyfile

global_email = "bganglia892@gmail.com"

class TestUnpywallCache:
    @pytest.fixture
    def example_cache(self):

        UnpywallCredentials(global_email)

        copyfile(os.path.join(test_dir, "example_cache"),
                 os.path.join(test_dir, "test_cache"))
        cache = UnpywallCache(os.path.join(test_dir, "test_cache"))
        assert cache.content != {}
        assert cache.access_times != {}
        return cache

    def test_reset_cache(self, example_cache):
        example_cache.reset_cache()
        assert example_cache.content == {}
        assert example_cache.access_times == {}

    def test_delete(self, example_cache):
        doi = "10.1016/j.jns.2020.116832"
        example_cache.delete(doi)
        assert doi not in example_cache.content
        assert doi not in example_cache.content

    def test_timeout(self, example_cache):
        timeout = 1
        doi = "10.1016/j.jns.2020.116832"
        example_cache.timeout = timeout
        assert doi not in example_cache.content
        example_cache.get(doi)
        time.sleep(timeout)
        assert example_cache.timed_out(doi)
