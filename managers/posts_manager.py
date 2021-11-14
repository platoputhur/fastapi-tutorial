from abc import abstractmethod, ABC

from sqlalchemy.orm import Session

from managers.database_manager import DatabaseManager
from managers.sqlalchemy_manager import get_db
from models.bal.schemas import PostCreateRequest, PostUpdateRequest
from models.dal.models import Post as ORMPost


class PostsManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_posts(self):
        pass

    @abstractmethod
    def get_post(self, post_id):
        pass

    @abstractmethod
    def create_post(self, post: PostCreateRequest):
        pass

    @abstractmethod
    def delete_post(self, post_id):
        pass

    @abstractmethod
    def update_post(self, post_id, post: PostUpdateRequest):
        pass


class PostsManagerFactory:
    def __call__(self, use_orm=True):
        if use_orm:
            return PostsManagerWithORM()
        else:
            return PostsManagerWithoutORM()


class PostsManagerWithORM(PostsManager):

    def get_posts(self):
        db: Session = get_db()
        posts = db.query(ORMPost).all()
        return posts

    def get_post(self, post_id):
        db: Session = get_db()
        post = db.query(ORMPost).filter_by(id=post_id).first()
        # post = db.query(ORMPost).filter(ORMPost.id == int(post_id)).first()
        return post

    def create_post(self, post: PostCreateRequest):
        db: Session = get_db()
        # This ** is just unpacking the dict which will work
        # because both the pydantic modal and the orm model
        # have the same keys and values for those classes
        # This way we don't have to manually type in all the keys
        new_post = ORMPost(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    def delete_post(self, post_id):
        db: Session = get_db()
        post = db.query(ORMPost).filter_by(id=post_id)
        deleted_post = post.first()
        if deleted_post is not None:
            post.delete(synchronize_session=False)
            db.commit()
        return deleted_post

    def update_post(self, post_id, post: PostUpdateRequest):
        db: Session = get_db()
        post_query = db.query(ORMPost).filter_by(id=post_id)
        post_to_update = post_query.first()
        if post_to_update is not None:
            post_query.update(post.dict(), synchronize_session=False)
            db.commit()
            db.refresh(post_to_update)
        return post_to_update


class PostsManagerWithoutORM(PostsManager):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()

    def get_posts(self):
        posts = self.db_manager.execute_query("select * from posts")
        return posts

    def get_post(self, post_id):
        post = self.db_manager.execute_query("SELECT * FROM posts WHERE id='%s'", (post_id,), single_record_flag=True)
        return post

    def create_post(self, post: PostCreateRequest):
        post = self.db_manager.execute_query("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *",
                                             (post.title, post.content), single_record_flag=True)

        return post

    def delete_post(self, post_id):
        post = self.db_manager.execute_query("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,),
                                             single_record_flag=True)
        return post

    def update_post(self, post_id, post: PostUpdateRequest):
        post = self.db_manager.execute_query(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s RETURNING *",
            (post.title, post.content, post.published, post_id),
            single_record_flag=True)
        return post
