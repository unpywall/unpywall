import pytest
import pandas as pd
import os
from requests.exceptions import HTTPError

from unpywall import Unpywall

os.environ['UNPAYWALL_EMAIL'] = 'nick.haupka@gmail.com'


class TestUnpywall:

    def test_validate_dois(self):

        correct_dois = ['10.1038/nature12373', '10.1103/physreve.88.012814']
        bad_dois = 'a bad doi'

        with pytest.raises(ValueError, match='No DOI specified'):
            assert Unpywall._validate_dois(None)

        with pytest.raises(ValueError,
                           match='The input format must be of type list'):
            assert Unpywall._validate_dois(bad_dois)

        with pytest.raises(ValueError,
                           match=('Unpaywall only allows to 100,000 calls'
                                  ' per day')):
            assert Unpywall._validate_dois(['doi'] * (Unpywall.api_limit + 1))

        assert Unpywall._validate_dois(correct_dois) == correct_dois

    def test_get_df(self):

        with pytest.raises(ValueError,
                           match=('The argument format only accepts the'
                                  ' values "raw" and "extended"')):
            assert Unpywall.get_df(dois=['10.1038/nature12373'],
                                   format='not a valid format')

        with pytest.raises(ValueError,
                           match=('The argument errors only accepts the values'
                                  ' "ignore" and "raise"')):
            assert Unpywall.get_df(dois=['10.1038/nature12373'],
                                   progress=False,
                                   errors='skip')

        df_raw = Unpywall.get_df(dois=['10.1038/nature12373'],
                                 format='raw',
                                 errors='ignore')

        assert isinstance(df_raw, pd.DataFrame)

        df_extended = Unpywall.get_df(dois=['10.1038/nature12373'],
                                      format='extended',
                                      errors='ignore')

        assert isinstance(df_extended, pd.DataFrame)

        with pytest.warns(UserWarning):
            df_empty = Unpywall.get_df(dois=['a bad doi'],
                                       errors='ignore')

            assert df_empty is None

    def test_get_json(self):

        with pytest.raises(HTTPError):
            Unpywall.get_json('a bad doi', errors='raise')

        with pytest.warns(UserWarning):
            Unpywall.get_json('a bad doi', errors='ignore')

        assert isinstance(Unpywall.get_json('10.1016/j.tmaid.2020.101663',
                                            errors='raise'), dict)

    def test_get_pdf_link(self):

        assert isinstance(Unpywall.get_pdf_link('10.1038/nature12373'), str)

    def test_get_doc_link(self):

        assert isinstance(
                Unpywall.get_doc_link('10.1016/j.tmaid.2020.101663'), str)

    def test_get_all_links(self):

        assert isinstance(
                Unpywall.get_all_links('10.1016/j.tmaid.2020.101663'), list)
