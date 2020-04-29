from unpywall.__main__ import main
from requests.exceptions import HTTPError
import pytest


class TestUnpywallCli:

    def test_main(self):
        with pytest.raises(SystemExit) as pytest_raise_system_exit:
            main(test_args=(['-h']))

        assert pytest_raise_system_exit.value.code == 0

        with pytest.raises(SystemExit) as pytest_raise_system_exit:
            main(test_args=(['this is a bad argument']))

        assert pytest_raise_system_exit.value.code == 1

    def test_view(self):
        with pytest.raises(SystemExit) as pytest_raise_system_exit:
            main(test_args=(['view']))

        assert pytest_raise_system_exit.value.code == 2

        with pytest.raises(HTTPError):
            bad_doi = 'this is a bad doi'
            main(test_args=(['view', bad_doi]))
