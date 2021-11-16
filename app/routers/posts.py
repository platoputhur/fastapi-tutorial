from typing import List

from fastapi import status, Response, APIRouter, Depends

from managers.auth_manager import verify_token_and_get_current_user
from managers.posts_manager import PostsManagerFactory
from models.bal.schemas import PostResponse, PostCreateRequest, PostUpdateRequest, UserResponse

posts_factory = PostsManagerFactory()
posts_manager = posts_factory()

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[PostResponse])
def get_posts(current_user: UserResponse = Depends(verify_token_and_get_current_user), limit: int = 10, skip: int = 0,
              search: str = ""):
    posts = posts_manager.get_posts(limit, skip, search)
    return posts


# How jwt access token verification works
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(new_post: PostCreateRequest, current_user: UserResponse = Depends(verify_token_and_get_current_user)):
    post = posts_manager.create_post(new_post, current_user.id)
    return post


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, current_user: UserResponse = Depends(verify_token_and_get_current_user)):
    # post = next((item for item in my_posts if item['id'] == post_id), None)
    post = posts_manager.get_post(post_id)
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id {post_id} doesn't exist"}
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: UserResponse = Depends(verify_token_and_get_current_user)):
    # index = find_index(post_id, my_posts)
    # if index is not None:
    #     my_posts.pop(index)
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {post_id} could not be found")
    posts_manager.delete_post(post_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdateRequest,
                current_user: UserResponse = Depends(verify_token_and_get_current_user)):
    post = posts_manager.update_post(post_id, post, current_user.id)
    return post
