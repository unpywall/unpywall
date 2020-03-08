import urllib.request
import json

email = None

class NoEmailException(Exception):
    pass

def _unpaywall_url(doi):
    search_url = "https://api.unpaywall.org/v2/{0}?email={1}".format(doi, email)
    return search_url

def unpaywall_json(doi):
    if email is None:
        raise NoEmailException("You must enter an email addresss.")
    with urllib.request.urlopen(_unpaywall_url(doi)) as handle:
        return json.read(handle)
