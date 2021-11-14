from typing import List

from fastapi import HTTPException, status, Response, APIRouter

from managers.posts_manager import PostsManagerFactory
from models.bal.schemas import PostResponse, PostCreateRequest, PostUpdateRequest

router = APIRouter()


@router.get("/posts", response_model=List[PostResponse])
def get_posts():
    posts = posts_manager.get_posts()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(new_post: PostCreateRequest):
    post = posts_manager.create_post(new_post)
    return post


posts_factory = PostsManagerFactory()
posts_manager = posts_factory()


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    # post = next((item for item in my_posts if item['id'] == post_id), None)
    post = posts_manager.get_post(post_id)
    if post is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {post_id} doesn't exist"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} doesn't exist")
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    # index = find_index(post_id, my_posts)
    # if index is not None:
    #     my_posts.pop(index)
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id {post_id} could not be found")
    post = posts_manager.delete_post(post_id)
    if post is not None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} could not be found")


@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdateRequest):
    post = posts_manager.update_post(post_id, post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {post_id} could not be found")
    else:
        return post
