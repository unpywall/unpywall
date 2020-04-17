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
            raise ValueError('An email address is required in order to'
                             + ' work with the Unpaywall API')

        if not re.match(email_regex, email):
            raise ValueError('No valid email address entered.'
                             + ' Enter a valid email address')

        if 'example.com' in email:
            raise ValueError('Do not use example.com')

        return email


class UnpywallURL:
    """
    This class provides the Unpaywall URL.

    Attributes
    ----------
    doi : str
        The desired DOI.
    url : str
        Constructs an Unpaywall URL
    """

    def __init__(self, doi: str) -> None:
        self.doi = doi

    @property
    def url(self) -> str:
        email = UnpywallCredentials \
                    .validate_email(os.environ.get('UNPAYWALL_EMAIL'))

        return 'https://api.unpaywall.org/v2/{0}?email={1}'.format(self.doi,
                                                                   email)
