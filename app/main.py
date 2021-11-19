from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, posts, auth, votes

# Creating the tables in the db
# probably best to move it to somewhere else
# as we don't want the server to try to create
# the tables at each restart.
# Base.metadata.create_all(bind=engine)
# The above line of code is not needed anymore because we are using the auto migrate tool: alembic

app = FastAPI()
# List of domains from which we have to enable cors requests
origins = ['*']
# List of methods like post, get etc in which we have to enable cors requests
methods = ['*']
app.add_middleware(CORSMiddleware,
                   allow_origin=origins,
                   allow_credentials=True,
                   allow_methods=methods,
                   allow_headers=["*"]
                   )
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# function name doesn't matter
# order of the routes matters, so if you have two same route paths
# the first one is going to run and that would be the end of it
# async key word is optional and its only required if you are doing
# some async operations, here we are not doing it, but giving it wouldn't
# cause any issue.
@app.get("/")
async def root():
    return {"message": "hello mate"}
