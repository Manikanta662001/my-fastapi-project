from fastapi import HTTPException, status
from app.api.utils.hashing import hash_password, verify_password
from app.database import users_collection
from app.api.utils.auth import create_access_token, create_refresh_token


def register_user(user):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        user_dict = user.dict()
        user_dict["password"] = hash_password(user.password)
        users_collection.insert_one(user_dict)
        return {"message": "User Registered Successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )


def login_user(user):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password Wrong"
        )
    data = {"sub": db_user["email"]}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {
        "message": "Login Successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


def get_all_users():
    users = list(users_collection.find({}, {"_id": 0, "password": 0}))
    return users
