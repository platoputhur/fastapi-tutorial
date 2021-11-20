import pytest

from models.bal.schemas import PostResponse, PostWithVotesResponse


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return PostWithVotesResponse(**post)

    list(map(validate, res.json()))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_get_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_non_existent_post(authorized_client, test_posts):
    res = authorized_client.get("/posts/454545")
    assert res.status_code == 404


def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = PostWithVotesResponse(**res.json())
    assert post.Post.id == str(test_posts[0].id)
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("creating post 1", "content for the post number 1", True),
    ("creating post 2", "content for the post number 2", False),
    ("creating post 3", "content for the post number 3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "published": published
    })

    created_post = PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user):
    res = authorized_client.post("/posts/", json={
        "title": "title1",
        "content": "content1",
    })
    created_post = PostResponse(**res.json())
    assert created_post.published is True


def test_unauthorized_create_post(client, test_posts):
    res = client.post("/posts/", json={
        "title": "title1",
        "content": "content1",
    })
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts, test_user):
    number_of_posts = len(test_posts)
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    res = authorized_client.get("/posts/")
    number_of_posts_after_deletion = len(res.json())
    assert number_of_posts == number_of_posts_after_deletion + 1


def test_delete_non_existent_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{2323434}")
    assert res.status_code == 404


def test_delete_post_owned_by_different_user(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "this is the updated post title",
        "content": "this is the updated post content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.id == str(test_posts[0].id)
    assert updated_post.title == "this is the updated post title"
    assert updated_post.content == "this is the updated post content"
    assert updated_post.published is False


def test_update_post_owned_by_different_user(authorized_client, test_posts, test_user):
    data = {
        "title": "this is the updated post title",
        "content": "this is the updated post content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_posts):
    data = {
        "title": "this is the updated post title",
        "content": "this is the updated post content",
        "published": False
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401


def test_delete_non_update_post(authorized_client, test_posts, test_user):
    data = {
        "title": "this is the updated post title",
        "content": "this is the updated post content",
        "published": False
    }
    res = authorized_client.put(f"/posts/454545454", json=data)
    assert res.status_code == 404
