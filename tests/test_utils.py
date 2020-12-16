import pytest

from unpywall.utils import UnpywallCredentials, UnpywallURL


class TestUnpywallCredentials:

    def test_validate_email(self):

        correct_email = 'nick.haupka@gmail.de'
        bad_email = 'https://github.com/naustica/unpywall'

        with pytest.raises(ValueError,
                           match=('An email address is required in order'
                                  ' to work with the Unpaywall API')):
            assert UnpywallCredentials.validate_email(None)

        with pytest.raises(ValueError,
                           match=('No valid email address entered.'
                                  ' Enter a valid email address')):
            assert UnpywallCredentials.validate_email(bad_email)

        with pytest.raises(ValueError, match='Do not use example.com'):
            assert UnpywallCredentials.validate_email(
              'nick.haupka@example.com')

        assert UnpywallCredentials.validate_email(
            correct_email) == correct_email

        assert isinstance(repr(UnpywallCredentials(correct_email)), str)

        assert isinstance(UnpywallCredentials(correct_email).email, str)


class TestUnpywallURL:

    def test_doi_url(self):

        doi = '10.1038/nature12373'

        url = UnpywallURL(doi=doi).doi_url

        assert isinstance(url, str)

    def test_query_url(self):

        query = 'duck'

        url = UnpywallURL(query=query).query_url

        assert isinstance(url, str)
