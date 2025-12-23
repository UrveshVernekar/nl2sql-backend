from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.query import router as query_router
from app.api.auth import router as auth_router
from app.api.chats import router as chats_router
from app.api.messages import router as messages_router


app = FastAPI(title="NL2SQL API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(query_router)
app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(messages_router)