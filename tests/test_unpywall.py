from unpywall import Unpywall


class TestUnpywall:

    def test_validate_dois(self):
        dois = ['10.1038/nature12373', '10.1103/physreve.88.012814']
        assert Unpywall._validate_dois(dois)

    def test_validate_email(self):
        email = 'nick.haupka@gmail.com'
        assert Unpywall._validate_email(email)
