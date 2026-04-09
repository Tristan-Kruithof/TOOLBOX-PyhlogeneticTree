import sys
sys.path.append('..')
import pytest
import html5lib
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user'] = {"email" : "detristank@gmail.com", "admin" : True, "active" : True, "newsletter" : True}  # fake user
        yield client


@pytest.mark.parametrize('uri', [
    '/'
    ,'/home'
    ,'/home/tools'
    , '/home/create'
    , '/home/compare'
    , '/home/DNA'
    , '/home/newsletter'
    , '/home/signup'
    , '/home/help/about'
    , '/home/help/installation'
    , '/home/help/contact'
])


def test_html_parse(client, uri):
    response = client.get(uri)
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=True, namespaceHTMLElements=False)
        parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)

