import pytest
import pandas as pd

from unpywall import Unpywall


class TestUnpywall:

    def test_validate_dois(self):

        correct_dois = ['10.1038/nature12373', '10.1103/physreve.88.012814']
        bad_dois = '10.1038/nature12373'

        with pytest.raises(ValueError, match='No DOI specified'):
            assert Unpywall._validate_dois(None)

        with pytest.raises(ValueError, match='The input format must be of type list'):
            assert Unpywall._validate_dois(bad_dois)

        assert Unpywall._validate_dois(correct_dois) == correct_dois

    def test_validate_email(self):

        correct_email = 'nick.haupka@google.de'
        bad_email = 'https://github.com/naustica/unpywall'

        with pytest.raises(ValueError, match='An email address is required in order to work with the Unpaywall API'):
            assert Unpywall._validate_email(None)

        with pytest.raises(ValueError, match='No valid email address entered. Enter a valid email address'):
            assert Unpywall._validate_email(bad_email)

        with pytest.raises(ValueError, match='Do not use example.com'):
            assert Unpywall._validate_email('nick.haupka@example.com')

        assert Unpywall._validate_email(correct_email) == correct_email

    def test_fetch(self):
        pass

    def test_parser(self):

        df = Unpywall._parser(dois=['10.1038/nature12373'],
                              email='nick.haupka@gmail.com',
                              progress=False,
                              errors='ignore')

        assert isinstance(df, pd.DataFrame)

    def test_get(self):

        with pytest.raises(ValueError, match='The argument errors only accepts the values "ignore" and "raise"'):
            assert Unpywall.get(dois=['10.1038/nature12373'],
                                email='nick.haupka@gmail.com',
                                progress=False,
                                errors='skip')
