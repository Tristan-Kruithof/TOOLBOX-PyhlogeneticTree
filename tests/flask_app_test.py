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


def test_create_add_organism(client):
    response = client.post('/home/create', data={
        'add' : 'true',
        'species' : "homo sapiens, mus musculus, gallus gallus, danio rerio"
    })
    assert response.status_code == 200


def test_create_too_few_organisms(client):
    response = client.post('/home/create', data={
        'input_method' : 'common',
        'gene' : 'COX1',
        'Graph' : 'Circular',
        'species' : 'homo sapiens'
    })
    assert b'Not enough species' in response.data


@pytest.mark.parametrize('uri', [
    # '/',
    '/'
    ,'/home'
    ,'/home/tools'
    , '/home/create'
    , '/home/compare'
    , '/home/newsletter'
    ,  '/home/signup'
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

    # forms = htmldoc.findall('./body/div/form')
    # assert len(forms) == 1
    # form = forms[0]
    # names = set()
    # for inp in form.iter('input'):
    #     names.add(inp.attrib['name'])
    # assert names == {'course', 'teacher', 'ec'}
