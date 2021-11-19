from abc import ABC, abstractmethod

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from managers.sqlalchemy_manager import get_db
from models.dal.models import Vote, Post


class VotesManagerFactory:
    def __call__(self, use_orm=True, *args, **kwargs):
        if use_orm:
            return VotesManagerWithORM()


class VotesManager(ABC):
    def __call__(self, *args, **kwargs):
        return VotesManagerWithORM()

    @abstractmethod
    def vote(self, vote_dir: int, post_id: int, user_id: int): pass


class VotesManagerWithORM(VotesManager):
    def vote(self, vote_dir: str, post_id: int, user_id: int):
        db: Session = get_db()
        votes_query = db.query(Vote).filter(Vote.post_id == post_id, Vote.user_id == user_id)
        found_vote = votes_query.first()
        if int(vote_dir) == 1:
            if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Current user has already voted on the post: {post_id}")
            post = db.query(Post).filter(Post.id == post_id).first()
            if post is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"The post: {post_id} doesn't exist")
            new_vote = Vote(post_id=post_id, user_id=user_id)
            db.add(new_vote)
            db.commit()
            return {"message": "successfully added vote"}
        else:
            if not found_vote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Vote doesn't exist for the post: {post_id}")
            else:
                votes_query.delete(synchronize_session=False)
                db.commit()
                return {"message": "successfully removed vote"}
