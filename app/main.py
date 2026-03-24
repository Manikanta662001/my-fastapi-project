from fastapi import FastAPI
from app.api.routes.user_routes import router as user_router
from app.api.routes.posts_routes import router as posts_router
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(user_router)
app.include_router(posts_router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
    