from fastapi import APIRouter, Depends
from app.api.models.user_model import RegisterUser, LoginUser, RefreshRequest
from app.api.controllers.user_controller import register_user, login_user, get_all_users
from app.api.utils.auth import verify_token, verify_refresh_token, create_access_token
from app.database import blacklist_collection

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", summary="To Register new User")
def register(user: RegisterUser):
    return register_user(user)

@router.post("/login", summary="To Login a User")
def login(user: LoginUser):
    return login_user(user)

@router.get("/users", summary="To get All Existing users")
def get_users(current_user = Depends(verify_token)):
    return get_all_users()

# 🔹 Refresh API
@router.post("/refresh")
def new_access_token(data: RefreshRequest):
    email = verify_refresh_token(data.refresh_token)
    new_access_token = create_access_token({"sub": email})
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(data: RefreshRequest):
    blacklist_collection.insert_one({
        "token": data.refresh_token
    })
    return {"message": "Logged out successfully"}