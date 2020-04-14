import requests
import urllib.request
import pickle
from copy import deepcopy
from abc import ABC, abstractmethod
import os
import pandas as pd
import json
import time
import sys
import re


class Unpaywall(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def url():
        pass


class UnpaywallCredentials:

    authentication_email = os.environ.get('UNPAYWALL_EMAIL')

    def __init__(self, email):
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, user_email):

        user_email = UnpaywallCredentials.validate_email(user_email)

        os.environ['UNPAYWALL_EMAIL'] = user_email

        self._email = user_email

    @staticmethod
    def validate_email(email):
        """
        The method takes an email as input and raises an error if the email is
        not valid. Otherwise the email will be returned.
        Parameters
        ----------
        email : str
            An email that is necessary for using the Unpaywall API service.
        Returns
        -------
        str
            The email that was given as input.
        Raises
        ------
        ValueError
            If the email parameter is empty or not valid.
        """

        # from https://stackoverflow.com/a/43937713/12580727
        email_regex = r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$'

        if email is None:
            raise ValueError('An email address is required in order to work with the Unpaywall API')

        if not re.match(email_regex, email):
            raise ValueError('No valid email address entered. Enter a valid email address')

        if 'example.com' in email:
            raise ValueError('Do not use example.com')

        return email


class UnpaywallURL(Unpaywall):

    def __init__(self, doi):
        super().__init__()
        self.doi = doi

    @property
    def url(self):
        email = UnpaywallCredentials.validate_email(UnpaywallCredentials.authentication_email)

        return 'https://api.unpaywall.org/v2/{0}?email={1}'.format(self.doi, email)


class UnpaywallCache:
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
                         'acces_times': self.access_times},
                        handle)

    def load(self, name=None):
        if not name:
            name = self.name
        with open(name, 'rb') as handle:
            data = pickle.load(handle)
        self.content = data['content']
        self.access_times = data['access_times']

    def download_again(self, doi):
        mandatory_wait_time = os.environ.get('MANDATORY_WAIT_TIME', 1)
        time.sleep(mandatory_wait_time)
        url = UnpaywallURL(doi).url
        return urllib.request.urlopen(url.read())


cache = UnpaywallCache()


class Unpywall:
    """
    Base class that contains useful functions for retrieving information
    from the Unpaywall REST API (https://api.unpaywall.org). This client uses
    version 2 of the API.

    Methods
    -------
    get(dois, email, progress, errors)
        Retrieves information from the Unpaywall API service and returns a
        pandas DataFrame.
    """

    api_limit = 100000

    @staticmethod
    def _fetch(doi, errors):
        """
        Fetches information from the Unpaywall API service.

        Parameters
        ----------
        doi : str
            The desired DOI.
        email : str
            An email that is necessary for using the Unpaywall API service.
        errors : str
            Either 'raise' or 'ignore'. If the parameter errors is set to
            'ignore' than errors will not raise an exception.

        Returns
        -------
        object
            A requests Response object.

        Raises
        ------
        HTTPError
            # TODO:
        RequestException
            # TODO:
        ConnectionError
            # TODO:
        Timeout
            # TODO:
        """
        try:
            url = UnpaywallURL(doi).url
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as HTTPError:
            if errors == 'raise':
                raise HTTPError

        except requests.exceptions.RequestException as RequestException:
            if errors == 'raise':
                raise RequestException

        except requests.exceptions.ConnectionError as ConnectionError:
            if errors == 'raise':
                raise ConnectionError

        except requests.exceptions.Timeout as Timeout:
            if errors == 'raise':
                raise Timeout

    @staticmethod
    def _validate_dois(dois):
        """
        The function accepts a list of DOIs and returns a cleaned version of it.
        Raises an error if the desired input is not given.
        Parameters
        ----------
        dois : list
            A list of DOIs. Each DOI should be represented as a string.
        Returns
        -------
        list
            A list of DOIs.
        Raises
        ------
        ValueError
            If the input is empty or not of type list.
        """
        if dois is None or len(dois) == 0:
            raise ValueError('No DOI specified')

        if not isinstance(dois, list):
            raise ValueError('The input format must be of type list')

        if len(dois) > Unpywall.api_limit:
            raise ValueError('Unpaywall only allows to 100,000 calls per day')

        for doi in dois:
            doi.replace(' ', '')

        return dois

    @staticmethod
    def _progress(progress):
        """
        The function prints out the current progress status of an API call.

        Parameters
        ----------
        progress : float
            Current status of the progress. Value between 0 and 1.
        """

        bar_len = 50
        block = int(round(bar_len*progress))

        text = '|{0}| {1}%'.format('=' * block + ' ' * (bar_len-block), int(progress * 100))

        print(text, end='\r', flush=False, file=sys.stdout)
        time.sleep(0.1)

    @staticmethod
    def get_df(dois, progress=False, errors='raise'):
        """
        Parses information from the Unpaywall API service and returns it as
        a pandas DataFrame.

        Parameters
        ----------
        dois : list
            A list of DOIs.
        email : str
            An email that is necessary for using the Unpaywall API service.
        progress : bool
            Whether the progress of the API call should be printed out.
        errors : str
            Either 'raise' or 'ignore'. If the parameter errors is set to
            'ignore' than errors will not raise an exception.

        Returns
        -------
        DataFrame
            A pandas DataFrame that contains information from the Unpaywall
            API service.

        Raises
        ------
        ValueError
            If the parameter errors contains a faulty value.
        AttributeError
            If the Unpaywall API did not respond with json.
        """

        dois = Unpywall._validate_dois(dois)

        if errors != 'ignore' and errors != 'raise':
            raise ValueError('The argument errors only accepts the values "ignore" and "raise"')

        df = pd.DataFrame()

        for n, doi in enumerate(dois, start=1):

            if progress:
                Unpywall._progress(n/len(dois))

            try:
                r = Unpywall._fetch(doi, errors).json()

                # check if json is not empty due to an faulty DOI
                if not bool(r):
                    continue

                df2 = pd.json_normalize(data=r, max_level=1, errors=errors)

                df = df.append(df2)

            except (AttributeError, json.decoder.JSONDecodeError):

                if errors == 'raise':
                    raise AttributeError('Unpaywall API did not return json')
                else:
                    continue

        return df

    @staticmethod
    def get_json(doi):
        """
        This function returns all information in Unpaywall about the given DOI.
        :param doi: The DOI of the requested paper.
        :returns: A JSON data structure containing all information returned by Unpaywall about the given DOI.
        """
        text = cache.get(doi)
        return json.loads(text)

    @staticmethod
    def unpaywall_pdf_link(doi):
        """
        This function returns a link to the an OA pdf (if available).
        :param doi: The DOI of the requested paper.
        :returns: The URL of an OA PDF (if available).
        """
        json_data = Unpywall.get_json(doi)
        try:
            return json_data["best_oa_location"]["url_for_pdf"]
        except (KeyError, TypeError):
            return None

    @staticmethod
    def unpaywall_doc_link(doi):
        """
        This function returns a link to the best OA location (not necessarily a PDF).
        :param doi: The DOI of the requested paper.
        :returns: The URL of the best OA location (not necessarily a PDF).
        """
        json_data = Unpywall.unpaywall_json(doi)
        try:
            return json_data["best_oa_location"]["url"]
        except (KeyError, TypeError):
            return None

    @staticmethod
    def unpaywall_all_links(doi):
        """
        This function returns a list of URLs for all open-access copies
        listed in Unpaywall.
        :param doi: The DOI of the requested paper.
        :returns: A list of URLs leading to open-access copies.
        """
        data = []
        for value in [Unpywall.unpaywall_doc_link(doi),
                      Unpywall.unpaywall_pdf_link(doi)]:
            if value and value not in data:
                data.append(value)
        return data

    @staticmethod
    def unpaywall_download_pdf_handle(doi):
        """
        This function returns a file-like object containing the requested PDF.
        :param doi: The DOI of the requested paper.
        :returns: The handnle of the PDF file.
        """
        pdf_link = Unpywall.unpaywall_pdf_link(doi)
        return urllib.request.urlopen(pdf_link)

    @staticmethod
    def unpaywall_download_requests(doi):
        """
        This function returns a pdf corresponding to the doi, as text.
        :param doi: The DOI of the requested paper
        :returns: The text of a PDF file
        """
        pdf_link = Unpywall.unpaywall_pdf_link(doi)
        return requests.get(pdf_link).text
