from models.bal import schemas
from tests.database import client, session


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "hello mate"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={
        "email": "damn@gmail.com",
        "password": "foobar2"
    })
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "damn@gmail.com"
    assert res.status_code == 201


def test_login(client):
    res = client.post("/login", data={"username": "damn@gmail.com", "password": "foobar2"})
    print(res.json())
    assert res.status_code == 200
