from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users.routers import router as user_router


app = FastAPI(root_path="/api/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
