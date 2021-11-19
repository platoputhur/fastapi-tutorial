from fastapi import status, APIRouter, Depends
from sqlalchemy.orm import Session

from managers.auth_manager import verify_token_and_get_current_user
from managers.sqlalchemy_manager import get_db
from managers.votes_manager import VotesManagerFactory
from models.bal.schemas import VoteRequest, UserResponse

router = APIRouter(prefix="/vote", tags=["Vote"])
votes_factory = VotesManagerFactory()
votes_manager = votes_factory()


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(user_vote: VoteRequest, current_user: UserResponse = Depends(verify_token_and_get_current_user),
         db: Session = Depends(get_db)):
    result = votes_manager.vote(user_vote.dir, user_vote.post_id, current_user.id)
    return result
