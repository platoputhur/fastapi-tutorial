# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# from app.main import app
# from helpers.config import settings
# from managers.sqlalchemy_manager import get_db
# from models.dal.models import Base
#
# # TEST DATABASE SETTINGS START
# SQLALCHEMY_TEST_DB_URL = settings.sqlalchemy_db_url + "_test"  # 'postgresql://postgres@127.0.0.1/fastapi'
#
# engine = create_engine(SQLALCHEMY_TEST_DB_URL)
# TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # TEST DATABASE SETTINGS END
# # RESET DATABASE CODE START
# @pytest.fixture()
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
#     db = TestSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @pytest.fixture()
# def client(session):
#     def override_get_db():
#         try:
#             yield session
#         finally:
#             session.close()
#
#     # Code which runs before our test
#     app.dependency_overrides[get_db] = override_get_db
#     yield TestClient(app)
#     # Code which runs after our test
#
# # RESET DATABASE CODE END
