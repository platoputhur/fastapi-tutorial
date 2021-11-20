import pytest
from jose import jwt

from helpers.config import settings
from models.bal import schemas
from models.bal.schemas import UserAuthenticationResponse


# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == "hello mate"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "damn@gmail.com",
        "password": "foobar2"
    })
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "damn@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    # Performing the login post request test
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert res.status_code == 200
    # Performing the token verification test to see if the returned token is valid and has the correct id
    # this must be done because token is sent from the server and so it must be validated/tested
    converted_res = UserAuthenticationResponse(**res.json())
    decoded_token = jwt.decode(converted_res.access_token, settings.auth_secret, algorithms=[settings.auth_algorithm])
    user_id = decoded_token.get("user_id")
    assert str(user_id) == test_user['id']
    # Check if the token type is bearer as the coder can think of changing the token type,
    # so it breaks the code. Here it must fail if it's changed
    assert converted_res.token_type == "bearer"


# Its best to try all possible scenarios
# So here try wrong email right password, and then right email, wrong password and then both wrong
@pytest.mark.parametrize("email, password, status_code", [
    ('boomer@gmail.com', 'fgdfgdfgd', 403),
    ('boome@gmail.cor', '1233455', 403),
    ('boome@gmail.cor', 'fgdfgdfgd', 403),
    ('', 'fgdfgdfgd', 422),
    ('boome@gmail.cor', '', 422),
    ('', '', 422),
    ('', None, 422),
    (None, '', 422),
    (None, None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid credentials."


def test_get_users(client, test_user):
    res = client.get("/users/")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0].get('email') == test_user['email']
    assert res.json()[0].get('id') == test_user['id']


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    assert res.json().get('email') == test_user['email']
    assert res.json().get('id') == test_user['id']
