"""
test_routes.py

pytests the routes within app.py

Auth: Tristan Kruithof
Date: 10/04/2026
Version: 1.0
PEP-8:
"""

import sys
sys.path.append('..')
import pytest
import html5lib
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # As we have a login state on the site most HTML5 is not visible if the user is not logged in.
        # So we must update the session 'user' to active.
        with client.session_transaction() as session:
            session['user'] = {"email" : "detristank@gmail.com", "admin" : True, "active" : True, "newsletter" : True}  # fake user
        yield client

# Create route

# Tests if it doesn't add a duplicate to the list
def test_add_duplicate_organism(client):
    with client.session_transaction() as sess:
        sess["organisms"] = ["lion"]

    client.post("/home/create",
                data={"add": "1", "species": "Lion", "gene": "COI", "Graph": "r", "input_method": "common"})

    with client.session_transaction() as sess:
        assert sess["organisms"].count("lion") == 1

# Tests adding an organism
def test_add_organism_to_session(client):
    client.post("/home/create", data={"add": "1", "species": "Lion", "gene": "COI", "Graph": "r", "input_method": "common"})
    with client.session_transaction() as sess:
        assert "lion" in sess["organisms"]

# Tests keeping the order in a list after adding an animal
def test_keeping_the_order_of_list_in_session(client):
    with client.session_transaction() as sess:
        sess["organisms"] = ["dog", "lion", "human"]

    client.post("/home/create", data={"add": "1", "species": "ape", "gene": "COI", "Graph": "r", "input_method": "common"})

    with client.session_transaction() as sess:
        assert sess["organisms"][-1] == 'ape'

# Tests adding multiple organisms at once
def test_add_organisms_to_session(client):
    client.post("/home/create", data={"add": "1", "species": "Lion, goat, horse", "gene": "COI", "Graph": "r", "input_method": "common"})
    with client.session_transaction() as sess:
        assert ['lion','goat', 'horse'] == sess["organisms"]

# Tests if it works when deleting just one organism.
def test_del_organism_in_session(client):
    with client.session_transaction() as sess:
        sess["organisms"] = ["lion", "tiger", "bear"]

    client.post("/home/create", data={"delete_org": "1", "species": "", "gene": "COI", "Graph": "r", "input_method": "common"})

    with client.session_transaction() as sess:
        assert ["lion", "tiger"] == sess["organisms"]

# Tests if it correctly works when deleting all organisms
def test_del_organisms_in_session(client):
    with client.session_transaction() as sess:
        sess["organisms"] = ["lion", "tiger", "bear"]

    client.post("/home/create", data={"delete_all": "1", "species": "", "gene": "COI", "Graph": "r", "input_method": "common"})

    with client.session_transaction() as sess:
        assert [] == sess["organisms"]

# Tests if it correctly works when there are too few organisms.
def test_too_few_organisms_shows_error(client):
    with client.session_transaction() as sess:
        sess["organisms"] = ["lion", "tiger"]

    response = client.post("/home/create", data={"run": "1", "gene": "COI", "Graph": "r", "input_method": "common"})
    assert b"Not enough species" in response.data

# DNA route
def test_dna_post_no_file_redirects(client):
    response = client.post("/home/DNA", data={})
    assert response.status_code in (200, 302)

# All the routes that need to be checked.
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

# Parses through all the HTML5 in an active login state so most HTML5 is visible
# And checks if this is valid HTML5
def test_html_parse(client, uri):
    response = client.get(uri)
    assert response.status_code == 200
    try:
        parser = html5lib.HTMLParser(strict=True, namespaceHTMLElements=False)
        parser.parse(response.data)
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f'{error.__class__.__name__}: {str(error)}', pytrace=False)