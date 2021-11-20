import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from helpers.config import settings
from helpers.oauth2_utils import create_access_token
from managers.sqlalchemy_manager import get_db
from models.dal.models import Base, Post

# TEST DATABASE SETTINGS START
SQLALCHEMY_TEST_DB_URL = settings.sqlalchemy_db_url + "_test"  # 'postgresql://postgres@127.0.0.1/fastapi'

engine = create_engine(SQLALCHEMY_TEST_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# TEST DATABASE SETTINGS END
# RESET DATABASE CODE START
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # Code which runs before our test
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Code which runs after our test


# RESET DATABASE CODE END


@pytest.fixture
def test_user(client):
    test_user_data = {
        "email": "boomer@gmail.com",
        "password": "1233455"
    }
    res = client.post("/users/", json=test_user_data)
    assert res.status_code == 201
    new_test_user = res.json()
    new_test_user["password"] = test_user_data["password"]
    return new_test_user


@pytest.fixture
def secondary_test_user(client):
    test_user_data = {
        "email": "fooper@gmail.com",
        "password": "1233455"
    }
    res = client.post("/users/", json=test_user_data)
    assert res.status_code == 201
    new_test_user = res.json()
    new_test_user["password"] = test_user_data["password"]
    return new_test_user


# Handling authorization
# To do this we will create the token for the test user manually instead of logging in
# and getting the token, that's an unnecessary db operation, so we will avoid it
# Then we will add this token to the clients header through another fixture
@pytest.fixture
def token(test_user):
    jwt_token = create_access_token(data={"user_id": test_user['id']})
    return jwt_token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# Handling posts
@pytest.fixture
def test_posts(test_user, secondary_test_user, session):
    posts_data = [
        {
            "title": "post title 1",
            "content": "post content 1",
            "owner_id": test_user['id']
        },
        {
            "title": "post title 2",
            "content": "post content 2",
            "owner_id": test_user['id']
        },
        {
            "title": "post title 3",
            "content": "post content 3",
            "owner_id": test_user['id']
        },
        {
            "title": "post title 4",
            "content": "post content 4",
            "owner_id": test_user['id']
        },
        {
            "title": "post title 5",
            "content": "post content 5",
            "owner_id": secondary_test_user['id']
        }
    ]

    def create_posts_model(post):
        return Post(**post)

    posts_map = map(create_posts_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()
    posts_list = session.query(Post).all()
    return posts_list
