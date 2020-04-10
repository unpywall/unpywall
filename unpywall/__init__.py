import requests
import pandas as pd
import json
import re
import time
import sys


class Unpywall:

    api_limit = 100000

    @staticmethod
    def _validate_dois(dois):
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
    def _validate_email(email):

        # from https://stackoverflow.com/a/43937713/12580727
        email_regex = r'^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$'

        if email is None:
            raise ValueError('An email address is required in order to work with the Unpaywall API')

        if not re.match(email_regex, email):
            raise ValueError('No valid email address entered. Enter a valid email address')

        if 'example.com' in email:
            raise ValueError('Do not use example.com')

        return email

    @staticmethod
    def _fetch(doi, email, errors):
        try:
            url = 'https://api.unpaywall.org/v2/{0}?email={1}'.format(doi, email)
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
    def _progress(progress):

        bar_len = 50
        block = int(round(bar_len*progress))

        text = '|{0}| {1}%'.format('=' * block + ' ' * (bar_len-block), int(progress * 100))

        print(text, end='\r', flush=False, file=sys.stdout)
        time.sleep(0.1)

    @staticmethod
    def _parser(dois, email, progress, errors):

        df = pd.DataFrame()

        for n, doi in enumerate(dois, start=1):

            if progress:
                Unpywall._progress(n/len(dois))

            try:
                r = Unpywall._fetch(doi, email, errors).json()

                if not bool(r):
                    continue

                df2 = pd.json_normalize(data=r, max_level=0, errors=errors)

                df = df.append(df2)

            except (AttributeError, json.decoder.JSONDecodeError):

                if errors == 'raise':
                    raise AttributeError('Unpaywall API did not return json')
                else:
                    continue

        return df

    @staticmethod
    def get(dois, email, progress=False, errors='raise'):

        dois = Unpywall._validate_dois(dois)
        email = Unpywall._validate_email(email)

        if errors != 'ignore' and errors != 'raise':
            raise ValueError('The argument errors only accepts the values "ignore" and "raise"')

        df = Unpywall._parser(dois, email, progress, errors)

        return df
