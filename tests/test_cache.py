import pytest
import os
test_dir = os.path.abspath(os.path.dirname(__file__))

from unpywall.cache import UnpywallCache
from requests.exceptions import HTTPError
from shutil import copyfile

class TestUnpywallCache:
    @pytest.fixture
    def example_cache(self):
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