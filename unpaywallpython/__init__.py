import urllib.request
import requests
import json
import time
import pickle
from copy import deepcopy
import os

email = None

_mandatory_wait_time = 1

class NoEmailException(Exception):
    pass

class UnpaywallCache():
    def __init__(self, timeout="never", name=None):
        if name == None:
            self.name = os.path.join(os.path.dirname(__file__),"unpaywall_cache")
        else:
            self.name = name
        try:
            self.load(self.name)
        except FileNotFoundError:
            print("no cache found")
            self.content = {}
            self.access_times = {}
        self.timeout = timeout
    def timed_out(self, doi):
        if self.timeout == "never":
            return False
        return time.time() > self.access_times[doi] + self.timeout
    def get(self, doi):
        if (not doi in self.content) or self.timed_out(doi):
            self.access_times[doi] = time.time()
            self.content[doi] = self.download_again(doi)
            self.save()
        return deepcopy(self.content[doi])
    def save(self, name=None):
        if name == None:
            name = self.name
        with open(self.name, "wb") as handle:
            pickle.dump({"content":self.content,
                         "access_times":self.access_times},
                        handle)
    def load(self, name=None):
        if name == None:
            name = self.name
        with open(name, "rb") as handle:
            data = pickle.load(handle)
        self.content = data["content"]
        self.access_times = data["access_times"]
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

def unpaywall_pdf_link(doi):
    """
    This function returns a link to the an OA pdf (if available).
    :param doi: The DOI of the requested paper.
    :returns: The URL of an OA PDF (if available).
    """
    json_data = unpaywall_json(doi)
    try:
        return json_data["best_oa_location"]["url_for_pdf"]
    except (KeyError, TypeError):
        return None

def unpaywall_doc_link(doi):
    """
    This function returns a link to the best OA location (not necessarily a PDF).
    :param doi: The DOI of the requested paper.
    :returns: The URL of the best OA location (not necessarily a PDF). 
    """
    json_data = unpaywall_json(doi)
    try:
        return json_data["best_oa_location"]["url"]
    except (KeyError, TypeError):
        return None

def unpaywall_all_links(doi):
    """
    This function returns a list of URLs for all open-access copies 
    listed in Unpaywall.
    :param doi: The DOI of the requested paper.
    :returns: A list of URLs leading to open-access copies.
    """
    data = []
    for value in [unpaywall_doc_link(doi),
                  unpaywall_pdf_link(doi)]:
        if value and not value in data:
            data.append(value)
    return data

def unpaywall_download_pdf_handle(doi):
    """
    This function returns a file-like object containing the requested PDF.
    :param doi: The DOI of the requested paper.
    :returns: The handnle of the PDF file.
    """
    pdf_link = unpaywall_pdf_link(doi)
    return urllib.request.urlopen(pdf_link)

def unpaywall_download_requests(doi):
    """
    This function returns a pdf corresponding to the doi, as text.
    :param doi: The DOI of the requested paper
    :returns: The text of a PDF file
    """
    pdf_link = unpaywall_pdf_link(doi)
    return requests.get(pdf_link).text
