from app.database import posts_collection
from bson import ObjectId
from fastapi import HTTPException, status

def get_all_posts(current_user):
    user_posts = list(posts_collection.find({ "owner" : current_user }))
    for post in user_posts:
        post["_id"] = str(post["_id"])
    return user_posts

def create_post(post, current_user):
    post_dict = post.dict()
    post_dict["owner"] = current_user
    posts_collection.insert_one(post_dict)
    return {"message": "Post created"}

def update_post(post_id, post, current_user):
    db_post = posts_collection.find_one({ "_id" : ObjectId(post_id)})
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post not found")
    posts_collection.update_one({ "_id" : ObjectId(post_id)}, { "$set" : post.dict() })
    return {"message": "Post Updated"}

def delete_post(post_id, current_user):
    db_post = posts_collection.find_one({ "_id" : ObjectId(post_id)})
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post not found")
    posts_collection.delete_one({ "_id" : ObjectId(post_id)})
    return {"message": "Post Deleted"}