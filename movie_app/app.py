from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Query,
    Depends,
    Path,
)
from typing import Annotated
from database import Base, engine
from schemas import (
    MovieRead,
    MovieCreate,
    MovieUpdate,
    WatchStatusSet)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)

@app.get("/movies", response_model=list[MovieRead])
def get_movies(skip: Annotated[int, Query(ge=0)] = 0,
               limit: Annotated[int, Query(gt=0)] = 100,
               is_watched:bool = None):
    pass

@app.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: Annotated[int, Path(gt=0)]):
    pass

@app.post("/movies", response_model=MovieRead)
def create_movie(movie: MovieCreate):
    pass

@app.put("/movies/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: Annotated[int, Path(gt=0)], movie: MovieUpdate):
    pass

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def get_movie(movie_id: Annotated[int, Path(gt=0)]):
    pass

@app.put("/movies/{movie_id}/watch-status")
def get_movie(movie_id: Annotated[int, Path(gt=0)], w_status: WatchStatusSet):
    pass

@app.delete("/movies/{movie_id}/watch-status")
def get_movie(movie_id: Annotated[int, Path(gt=0)], w_status: WatchStatusSet):
    pass