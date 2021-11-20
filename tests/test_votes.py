import pytest

from models.dal.models import Vote


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    payload = {
        "post_id": test_posts[0].id,
        "dir": 1
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 201


def test_vote_on_post_twice(authorized_client, test_posts, test_vote):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 1
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    payload = {
        "post_id": test_posts[3].id,
        "dir": 0
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 201


def test_delete_vote_on_post_without_vote(authorized_client, test_posts, test_user):
    payload = {
        "post_id": test_posts[0].id,
        "dir": 0
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 404


def test_vote_on_non_existent_post(authorized_client, test_user):
    payload = {
        "post_id": 24545454,
        "dir": 1
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 404


def test_delete_vote_on_non_existent_post(authorized_client, test_user):
    payload = {
        "post_id": 24545454,
        "dir": 0
    }
    res = authorized_client.post("/vote/", json=payload)
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    payload = {
        "post_id": test_posts[0].id,
        "dir": 0
    }
    res = client.post("/vote/", json=payload)
    assert res.status_code == 401
