from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from fastapi import FastAPI, status # type: ignore

from .Routers import post, user, like, auth
# from .config import settings
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    informations = {
        "API Name": "Post-Vote APP",
        "Description": "This is a simple API for voting on posts",
        "Endpoints": "/posts, /users, /likes, /auth",
        "API Documenation": "/docs",
        "Version": "1.98.9",
        "Created By": "Sumit Dubey",
        "Contact": "sumitdubey810@outlook.com",
        "Tools used": {
            "Backend": "FastAPI",
            "Database": "PostgreSQL",
            "IDE": "Virtual Studio Code (VS Code)"
        },
        "The project was developed in": "3 days",
        "Start Date": "14-03-25",
        "End Date": ""
    }

    return JSONResponse(content=informations, status_code=200)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(like.router)
app.include_router(auth.router)
