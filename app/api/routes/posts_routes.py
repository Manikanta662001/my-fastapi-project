from fastapi import APIRouter, Depends
from app.api.models.posts_model import CreatePost, UpdatePost
from app.api.controllers.posts_controller import create_post, get_all_posts, update_post, delete_post
from app.api.utils.auth import verify_token

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", summary="To get all posts of current user")
def get_all(current_user = Depends(verify_token)):
    return get_all_posts(current_user)

@router.post("/create", summary="To create new post")
def create(post: CreatePost, current_user = Depends(verify_token)):
    return create_post(post, current_user)

@router.put("/update/{post_id}", summary="To update existing post")
def update(post_id: str, post: UpdatePost, current_user = Depends(verify_token)):
    return update_post(post_id, post, current_user)

@router.delete("/delete/{post_id}", summary="To Delete existing post")
def delete(post_id: str,current_user = Depends(verify_token)):
    return delete_post(post_id, current_user)