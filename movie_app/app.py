from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Query,
    Depends,
    Path,
)
from typing import Annotated

from starlette.status import HTTP_404_NOT_FOUND

from database import Base, engine, SessionLocal, get_db
from schemas import (
    MovieRead,
    MovieCreate,
    MovieUpdate,
    WatchStatusSet)
import crud

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)

@app.get("/movies", response_model=list[MovieRead])
def get_movies(
        db: Annotated[SessionLocal, Depends(get_db)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(gt=0)] = 100,
        is_watched:bool = None
):
    movie = crud.get_movies(db, skip=skip, limit=limit, is_watched=is_watched)
    return movie

@app.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie_id: Annotated[int, Path(gt=0)]
):
    movie = crud.get_movies(db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return movie

@app.post("/movies", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
def create_movie(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie: MovieCreate
):
    movie = crud.create_movie(db,movie)
    return movie

@app.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie_id: Annotated[int, Path(gt=0)],
        movie: MovieUpdate
):
    movie = crud.update_movie(db, movie_id, movie)
    return movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie_id: Annotated[int, Path(gt=0)]
):
    res = crud.delete_movie(db,movie_id)
    if not res:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

@app.put("/movies/{movie_id}/watch-status")
def set_status(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie_id: Annotated[int, Path(gt=0)],
        w_status: WatchStatusSet
):
    res = crud.set_status(db, movie_id)
    if not res:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

@app.delete("/movies/{movie_id}/watch-status")
def remove_status(
        db: Annotated[SessionLocal, Depends(get_db)],
        movie_id: Annotated[int, Path(gt=0)],
        w_status: WatchStatusSet
):
    res = crud.remove_status(db, movie_id)
    if not res:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)