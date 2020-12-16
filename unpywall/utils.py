import os
import re


class UnpywallCredentials:
    """
    This class provides tools for setting up an email for the
    Unpaywall service.

    Attributes
    ----------
    email : str
        An email that is necessary for using the Unpaywall API service.
    """

    def __init__(self, email: str) -> None:
        self.email = email

    def __repr__(self) -> str:
        return 'Your email has been set.'

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, user_email: str) -> None:

        user_email = UnpywallCredentials.validate_email(user_email)

        os.environ['UNPAYWALL_EMAIL'] = user_email

        self._email = user_email

    @staticmethod
    def validate_email(email: str) -> str:
        """
        This method takes an email as input and raises an error if the email is
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
            raise ValueError(('An email address is required in order'
                              ' to work with the Unpaywall API'))

        if not re.match(email_regex, email):
            raise ValueError(('No valid email address entered. Enter a'
                              ' valid email address'))

        if 'example.com' in email:
            raise ValueError('Do not use example.com')

        return email


class UnpywallURL:
    """
    This class provides the Unpaywall URL.

    Attributes
    ----------
    doi : str
        The DOI of the requested paper.
    query : str
        The text to search for.
    is_oa : bool
        A boolean value indicating whether the returned records should be
        Open Access or not.
    doi_url : str
        The URL for the DOI-Endpoint.
    query_url : str
        The URL for the Query-Endpoint
    """

    def __init__(self,
                 doi: str = None,
                 query: str = None,
                 is_oa: bool = False) -> None:

        self.doi = doi
        self.query = query
        self.is_oa = is_oa
        self.email = UnpywallCredentials.validate_email(
            os.environ.get('UNPAYWALL_EMAIL'))

    @property
    def doi_url(self) -> str:

        if self.doi is None:
            raise ValueError('Missing DOI')

        return 'https://api.unpaywall.org/v2/{0}?email={1}'.format(self.doi,
                                                                   self.email)

    @property
    def query_url(self) -> str:

        if self.query is None:
            raise ValueError('Missing query')
        return ('https://api.unpaywall.org/v2/search/?query={0}&is_oa={1}'
                '&email={2}').format(self.query, self.is_oa, self.email)
