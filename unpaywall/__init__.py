import urllib.request
import json
import time
from copy import deepcopy

email = None

_mandatory_wait_time = 1

class NoEmailException(Exception):
    pass

class UnpaywallCache():
    def __init__(self, timeout=100000000):
        self.timeout = timeout
        self.content = {}
        self.access_times = {}
    def timed_out(self, doi):
        return time.time() > self.access_times[doi] + self.timeout
    def get(self, doi):
        if (not doi in self.content) or self.timed_out(doi):
            self.access_times[doi] = time.time()
            self.content[doi] = self.download_again(doi)
        return deepcopy(self.content[doi])
    def download_again(self, doi):
        if email is None:
            raise NoEmailException("You must enter an email addresss.")
        time.sleep(_mandatory_wait_time)
        return urllib.request.urlopen(_unpaywall_url(doi)).read()

cache = UnpaywallCache()

def _unpaywall_url(doi):
    search_url = "https://api.unpaywall.org/v2/{0}?email={1}".format(doi, email)
    return search_url

def unpaywall_json(doi):
    text = cache.get(doi)
    return json.loads(text)
