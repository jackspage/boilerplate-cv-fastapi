# backend/main.py

import uvicorn

from fastapi import FastAPI

from api import notes
import api.utils as utils
import api.upload as upload
from database.db import engine, metadata, database

metadata.create_all(engine)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(utils.router, prefix='/transfer/{style}', tags=["styles"])
    application.include_router(upload.router, prefix='/upload', tags=["upload"])
    application.include_router(notes.router, prefix="/notes", tags=["notes"])
    return application


app = create_application()

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
