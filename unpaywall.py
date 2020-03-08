import urllib.request

email = None

class NoEmailException(Exception):
    pass

def _unpaywall_url(doi):
    if email is None:
        raise NoEmailException("You must enter an email addresss.")
    search_url = "https://api.unpaywall.org/v2/{0}?email={1}".format(doi, email)
    return search_url
