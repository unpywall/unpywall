import pytest
import pandas as pd
import os
from requests.exceptions import HTTPError

from unpywall import Unpywall
from unpywall.utils import UnpywallCredentials


class TestUnpywall:

    def test_validate_dois(self):

        correct_dois = ['10.1038/nature12373', '10.1103/physreve.88.012814']
        bad_dois = '10.1038/nature12373'

        with pytest.raises(ValueError, match='No DOI specified'):
            assert Unpywall._validate_dois(None)

        with pytest.raises(ValueError,
                           match='The input format must be of type list'):
            assert Unpywall._validate_dois(bad_dois)

        assert Unpywall._validate_dois(correct_dois) == correct_dois

    def test_validate_email(self):

        correct_email = 'nick.haupka@gmail.de'
        bad_email = 'https://github.com/naustica/unpywall'

        with pytest.raises(ValueError,
                           match='An email address is required in order to'
                                 + ' work with the Unpaywall API'):
            assert UnpywallCredentials.validate_email(None)

        with pytest.raises(ValueError,
                           match='No valid email address entered.'
                                 + ' Enter a valid email address'):
            assert UnpywallCredentials.validate_email(bad_email)

        with pytest.raises(ValueError, match='Do not use example.com'):
            assert UnpywallCredentials \
                    .validate_email('nick.haupka@example.com')

        assert UnpywallCredentials.validate_email(
                                        correct_email) == correct_email

    def test_fetch(self):
        pass

    @pytest.fixture
    def test_get_df(self):

        os.environ['UNPAYWALL_EMAIL'] = 'nick.haupka@gmail.com'

        with pytest.raises(ValueError,
                           match='The argument errors only accepts the'
                                 + ' values "ignore" and "raise"'):
            assert Unpywall.get_df(dois=['10.1038/nature12373'],
                                   progress=False,
                                   errors='skip')

        df = Unpywall.get_df(dois=['10.1038/nature12373'],
                             progress=False,
                             errors='ignore')

        assert isinstance(df, pd.DataFrame)

    def test_get_json(self):

        os.environ['UNPAYWALL_EMAIL'] = 'bganglia892@gmail.com'

        with pytest.raises(HTTPError):
            Unpywall.get_json('10.1016/j.tmaid', 'raise')

        with pytest.warns(UserWarning):
            Unpywall.get_json('10.1016/j.tmaid', 'ignore')

        assert isinstance(Unpywall.get_json('10.1016/j.tmaid.2020.101663',
                                            'raise'), dict)
