import pytest
import pandas as pd
import os
from io import BytesIO
from requests.exceptions import HTTPError

from unpywall import Unpywall
from unpywall.cache import UnpywallCache

test_cache = UnpywallCache(os.path.join(
                            os.path.abspath(
                                os.path.dirname(__file__)),
                                'unpaywall_cache'))

os.environ['UNPAYWALL_EMAIL'] = 'nick.haupka@gmail.com'


class TestUnpywall:

    @pytest.fixture
    def Unpywall(self):
        Unpywall.init_cache(test_cache)
        yield Unpywall

    def test_init_cache(self):

        Unpywall.init_cache()
        path = os.path.join(os.getcwd(), 'unpaywall_cache')
        assert Unpywall.cache.name == path
        os.remove(path)

        with pytest.raises(AttributeError,
                           match='Cache is not of type {0}'.format(
                                                            UnpywallCache)):
            assert Unpywall.init_cache('Not a UnpywallCache object.')

        Unpywall.init_cache(test_cache)
        assert os.path.exists(Unpywall.cache.name)

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

    def test_get_df(self, Unpywall, capfd):

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
                                 progress=True,
                                 errors='ignore')

        captured = capfd.readouterr()

        assert len(captured.out) > 0
        assert isinstance(df_raw, pd.DataFrame)

        df_extended = Unpywall.get_df(dois=['10.1038/nature12373'],
                                      format='extended',
                                      errors='ignore')

        assert isinstance(df_extended, pd.DataFrame)

        with pytest.warns(UserWarning):
            df_empty = Unpywall.get_df(dois=['a bad doi'],
                                       errors='ignore')

            assert df_empty is None

    def test_get_json(self, Unpywall):

        with pytest.raises(HTTPError):
            Unpywall.get_json('a bad doi', errors='raise')

        with pytest.warns(UserWarning):
            Unpywall.get_json('a bad doi', errors='ignore')

        assert isinstance(Unpywall.get_json('10.1016/j.tmaid.2020.101663',
                                            errors='raise'), dict)

    def test_get_pdf_link(self, Unpywall):

        assert isinstance(Unpywall.get_pdf_link('10.1038/nature12373'), str)

    def test_get_doc_link(self, Unpywall):

        assert isinstance(
                Unpywall.get_doc_link('10.1016/j.tmaid.2020.101663'), str)

    def test_get_all_links(self, Unpywall):

        assert isinstance(
                Unpywall.get_all_links('10.1016/j.tmaid.2020.101663'), list)

    def test_download_pdf_handle(self, Unpywall):

        assert isinstance(
                Unpywall.download_pdf_handle('10.1038/nature12373'), BytesIO)

    def test_progress(self, Unpywall, capfd):
        Unpywall._progress(0.5)
        captured = capfd.readouterr()
        assert len(captured.out) > 0

    def test_view_pdf(self, Unpywall):
        pass

    def test_download_pdf_file(self, Unpywall, capfd):

        filename = 'test.pdf'
        filepath = './test_dir'

        Unpywall.download_pdf_file('10.1038/nature12373',
                                   filename=filename,
                                   filepath=filepath,
                                   progress=True)

        captured = capfd.readouterr()
        assert len(captured.out) > 0

        path = os.path.join(filepath, filename)
        assert os.path.exists(path)

        os.remove(path)
        os.rmdir(filepath)
