from fastapi import FastAPI
from app.api.routes.user_routes import router as user_router
from app.api.routes.posts_routes import router as posts_router
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    servers=[{"url": "https://localhost:8000"}, {"url": "http://localhost:8000"}]
)

app.include_router(user_router)
app.include_router(posts_router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
