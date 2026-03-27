from app.database import posts_collection
from bson import ObjectId
from fastapi import HTTPException, status
from uuid import uuid4
from app.api.utils.image_upload import image_upload, UPLOAD_DIR
import os


def get_all_posts(current_user):
    user_posts = list(posts_collection.find({"owner": current_user}))
    for post in user_posts:
        post["_id"] = str(post["_id"])
    return user_posts


def create_post(title, content, image, current_user):
    post_dict = {"title": title, "content": content, "owner": current_user}
    if image:
        file_name = image_upload(image)
        post_dict["image"] = file_name
    posts_collection.insert_one(post_dict)
    return {"message": "Post created"}


def update_post(post_id, title, content, image, current_user):
    db_post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    update_data = {"title": title, "content": content}
    if image:
        if "image" in db_post:
            old_path = os.path.join(UPLOAD_DIR, db_post["image"])
            if os.path.exists(old_path):
                os.remove(old_path)

        # save new image
        file_name = image_upload(image)
        update_data["image"] = file_name
    posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": update_data})
    return {"message": "Post Updated"}


def delete_post(post_id, current_user):
    db_post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if "image" in db_post:
        existing_path = os.path.join(UPLOAD_DIR, db_post["image"])
        if os.path.exists(existing_path):
            os.remove(existing_path)

    posts_collection.delete_one({"_id": ObjectId(post_id)})
    return {"message": "Post Deleted"}
