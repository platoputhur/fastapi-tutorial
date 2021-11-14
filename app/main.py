from fastapi import FastAPI

from app.routers import users, posts
from managers.sqlalchemy_manager import engine
from models.dal.models import Base

# Creating the tables in the db
# probably best to move it to somewhere else
# as we don't want the server to try to create
# the tables at each restart.
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)


# function name doesn't matter
# order of the routes matters, so if you have two same route paths
# the first one is going to run and that would be the end of it
# async key word is optional and its only required if you are doing
# some async operations, here we are not doing it, but giving it wouldn't
# cause any issue.
@app.get("/")
async def root():
    return {"message": "hello mate"}
