import requests
import pickle
from copy import deepcopy
import os
import time


class UnpywallCache:
    """
    This class stores query results from Unpaywall.
    It has a configurable timeout that can also be set to never expire.
    """

    def __init__(self, timeout='never', name=None):
        if not name:
            self.name = os.path.join(os.getcwd(), 'unpaywall_cache')
        else:
            self.name = name
        try:
            self.load(self.name)
        except FileNotFoundError:
            print('No cache found')
            self.content = {}
            self.access_times = {}
        self.timeout = timeout

    def timed_out(self, doi):
        if self.timeout == 'never':
            return False
        return time.time() > self.access_times[doi] + self.timeout

    def get(self, doi):
        if (doi not in self.content) or self.timed_out(doi):
            self.access_times[doi] = time.time()
            self.content[doi] = self.download_again(doi)
            self.save()
        return deepcopy(self.content[doi])

    def save(self, name=None):
        if not name:
            name = self.name
        with open(self.name, 'wb') as handle:
            pickle.dump({'content': self.content,
                         'access_times': self.access_times},
                        handle)

    def load(self, name=None):
        if not name:
            name = self.name
        with open(name, 'rb') as handle:
            data = pickle.load(handle)
        self.content = data['content']
        self.access_times = data['access_times']

    def download_again(self, doi):

        from .utils import UnpywallURL

        mandatory_wait_time = os.environ.get('MANDATORY_WAIT_TIME', 1)
        time.sleep(mandatory_wait_time)
        url = UnpywallURL(doi).url
        return requests.get(url)

cache = UnpywallCache()
