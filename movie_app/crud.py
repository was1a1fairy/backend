from database import SessionLocal
from sqlalchemy import select
from models import Movie
from schemas import (
    MovieUpdate,
    MovieRead,
    MovieCreate,
    WatchStatusSet
)

def get_movies(
        db:SessionLocal,
        skip:int,
        limit:int,
        is_watched:bool
)->list[Movie]:
    statement = select(Movie).offset(skip).limit(limit)
    if is_watched is not None:
        statement = statement.where(Movie.is_watched == is_watched)
        return db.execute(statement).scalars().all()