from abc import abstractmethod, ABC

from fastapi import HTTPException, status
from sqlalchemy import func

from managers.database_manager import DatabaseManager
from models.bal.schemas import PostCreateRequest, PostUpdateRequest
from models.dal.models import Post, Vote


class PostsManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_posts(self, *args):
        pass

    @abstractmethod
    def get_post(self, post_id, db):
        pass

    @abstractmethod
    def create_post(self, post: PostCreateRequest, current_user_id: int, db):
        pass

    @abstractmethod
    def delete_post(self, post_id, current_user_id: int, db):
        pass

    @abstractmethod
    def update_post(self, post_id, post: PostUpdateRequest, current_user_id: int, db):
        pass


class PostsManagerFactory:
    def __call__(self, use_orm=True, *args, **kwargs):
        if use_orm:
            return PostsManagerWithORM()
        else:
            return PostsManagerWithoutORM()


class PostsManagerWithORM(PostsManager):

    def get_posts(self, limit, skip, search, db):
        # posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
        results = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id,
                                                                               isouter=True).group_by(
            Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
        return results

    def get_post(self, post_id, db):
        post = db.query(Post, func.count(Vote.post_id).label("votes")).join(Vote, Vote.post_id == Post.id,
                                                                            isouter=True).group_by(
            Post.id).filter(Post.id == post_id).first()
        print(post)
        # post = db.query(Post).filter(Post.id == int(post_id)).first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id {post_id} doesn't exist")
        return post

    def create_post(self, post: PostCreateRequest, current_user_id: int, db):
        # This ** is just unpacking the dict which will work
        # because both the pydantic modal and the orm model
        # have the same keys and values for those classes
        # This way we don't have to manually type in all the keys
        new_post = Post(owner_id=current_user_id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    def delete_post(self, post_id, current_user_id, db):
        post_query = db.query(Post).filter_by(id=post_id)
        post = post_query.first()
        if post is not None:
            if post.owner_id == current_user_id:
                post_query.delete(synchronize_session=False)
                db.commit()
                return post
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Forbidden operation.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id {post_id} could not be found")

    def update_post(self, post_id, post: PostUpdateRequest, current_user_id: int, db):
        post_query = db.query(Post).filter_by(id=post_id)
        post_to_update = post_query.first()
        if post_to_update is not None:
            if post_to_update.owner_id == current_user_id:
                post_query.update(post.dict(), synchronize_session=False)
                db.commit()
                db.refresh(post_to_update)
                return post_to_update
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Forbidden operation.")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id {post_id} could not be found")


class PostsManagerWithoutORM(PostsManager):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()

    def get_posts(self):
        posts = self.db_manager.execute_query("select * from posts")
        return posts

    def get_post(self, post_id, db):
        post = self.db_manager.execute_query("SELECT * FROM posts WHERE id='%s'", (post_id,), single_record_flag=True)
        return post

    def create_post(self, post: PostCreateRequest, current_user_id: int, db):
        post = self.db_manager.execute_query("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *",
                                             (post.title, post.content), single_record_flag=True)

        return post

    def delete_post(self, post_id, current_user_id, db):
        post = self.db_manager.execute_query("DELETE FROM posts WHERE id = %s RETURNING *", (post_id,),
                                             single_record_flag=True)
        return post

    def update_post(self, post_id, post: PostUpdateRequest, current_user_id, db):
        post = self.db_manager.execute_query(
            "UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s RETURNING *",
            (post.title, post.content, post.published, post_id),
            single_record_flag=True)
        return post
