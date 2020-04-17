import urllib.request
import pandas as pd
import json
import time
import sys


class Unpywall:
    """
    Base class that contains useful functions for retrieving information
    from the Unpaywall REST API (https://api.unpaywall.org). This client uses
    version 2 of the API.

    Methods
    -------
    get_df(dois, progress, errors)
        Retrieves information from the Unpaywall API service and returns a
        pandas DataFrame.
    """

    api_limit: int = 100000

    @staticmethod
    def _validate_dois(dois: list) -> list:
        """
        This method accepts a list of DOIs and returns a cleaned version of it.
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
    def _progress(progress: float) -> None:
        """
        This method prints out the current progress status of an API call.

        Parameters
        ----------
        progress : float
            Current status of the progress. Value between 0 and 1.
        """

        bar_len = 50
        block = int(round(bar_len*progress))

        text = '|{0}| {1}%'.format('=' * block + ' ' * (bar_len-block),
                                   int(progress * 100))

        print(text, end='\r', flush=False, file=sys.stdout)
        time.sleep(0.1)

        if progress == 1:
            print('\n', file=sys.stdout)

    @staticmethod
    def get_df(dois: list,
               progress: bool = False,
               errors: str = 'raise',
               ignore_cache: bool = True) -> pd.DataFrame:
        """
        Parses information from the Unpaywall API service and returns it as
        a pandas DataFrame.

        Parameters
        ----------
        dois : list
            A list of DOIs.
        progress : bool
            Whether the progress of the API call should be printed out or not.
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
            raise ValueError('The argument errors only accepts the'
                             + ' values "ignore" and "raise"')

        df = pd.DataFrame()

        for n, doi in enumerate(dois, start=1):

            if progress:
                Unpywall._progress(n/len(dois))

            try:
                r = Unpywall.get_json(doi,
                                      errors=errors,
                                      ignore_cache=ignore_cache)

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
    def get_json(doi: str,
                 errors: str = 'raise',
                 ignore_cache: bool = False):
        """
        This function returns all information in Unpaywall about the given DOI.

        Parameters
        ----------
        doi : str
            The DOI of the requested paper.

        Returns
        -------
        JSON object
            A JSON data structure containing all information
            returned by Unpaywall about the given DOI.
        """
        from .cache import cache

        r = cache.get(doi, errors, ignore_cache)
        if r:
            return r.json()
        else:
            return None

    @staticmethod
    def get_pdf_link(doi: str, errors: str = 'raise'):
        """
        This function returns a link to the an OA pdf (if available).

        Parameters
        ----------
        doi: str
            The DOI of the requested paper.

        Returns
        -------
        str
            The URL of an OA PDF (if available).
        """
        json_data = Unpywall.get_json(doi, errors=errors)
        try:
            return json_data['best_oa_location']['url_for_pdf']
        except (KeyError, TypeError):
            return None

    @staticmethod
    def get_doc_link(doi: str, errors: str = 'raise'):
        """
        This function returns a link to the best OA location
        (not necessarily a PDF).

        Parameters
        ----------
        doi : str
            The DOI of the requested paper.

        Returns
        -------
        str
            The URL of the best OA location (not necessarily a PDF).
        """
        json_data = Unpywall.get_json(doi, errors)
        try:
            return json_data['best_oa_location']['url']
        except (KeyError, TypeError):
            return None

    @staticmethod
    def get_all_links(doi: str, errors: str = 'raise') -> list:
        """
        This function returns a list of URLs for all open-access copies
        listed in Unpaywall.

        Parameters
        ----------
        doi : str
            The DOI of the requested paper.

        Returns
        -------
        list
            A list of URLs leading to open-access copies.
        """
        data = []
        for value in [Unpywall.get_doc_link(doi, errors),
                      Unpywall.get_pdf_link(doi, errors)]:
            if value and value not in data:
                data.append(value)
        return data

    @staticmethod
    def download_pdf_handle(doi: str, errors: str = 'raise'):
        """
        This function returns a file-like object containing the requested PDF.

        Parameters
        ----------
        doi : str
            The DOI of the requested paper.

        Returns
        -------
        object
            The handle of the PDF file.
        """
        pdf_link = Unpywall.get_pdf_link(doi, errors)
        return urllib.request.urlopen(pdf_link)
