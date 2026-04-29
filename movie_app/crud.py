from database import SessionLocal
from sqlalchemy import select
from models import Movie
from schemas import (
    MovieUpdate,
    MovieRead,
    MovieCreate
)

def get_movies(
        db:SessionLocal,
        movie_id:int | None,
        skip:int|None = 0,
        limit:int|None = 100,
        is_watched:bool|None = None
) -> list[Movie] | Movie:
    statement = select(Movie).offset(skip).limit(limit)
    if is_watched is not None:
        statement = statement.where(Movie.is_watched == is_watched)
    elif movie_id is not None:
        statement = statement.where(Movie.id == movie_id)
    return db.execute(statement).scalars().all()


def create_movie(
        db:SessionLocal,
        movie:MovieCreate
) -> Movie:
    movie = Movie(
        title=movie.title,
        genre=movie.genre,
        release_year=movie.genre,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(
        db:SessionLocal,
        movie_id:int,
        movie:MovieUpdate,
) -> MovieRead | bool:
    old_movie = db.get(Movie,movie_id)
    if old_movie is None:
        return False
    for field in movie:
        if field[1]:
            old_movie.field = field[1]
    db.commit()
    db.refresh(old_movie)
    return old_movie


def delete_movie(
        db:SessionLocal,
        movie_id:int,
) -> bool:
    movie = db.get(Movie,movie_id)
    if movie is None:
        return False
    db.delete(movie)
    db.commit()
    return True



def set_status(
        db: SessionLocal,
        movie_id:int,
) -> bool:
    movie = db.get(Movie,movie_id)
    if movie is None:
        return False
    movie.is_watched = 1
    db.commit()
    db.refresh(movie)
    return True


def remove_status(
        db:SessionLocal,
        movie_id:int,
) -> bool:
    movie = db.get(Movie, movie_id)
    if movie is None:
        return False
    movie.is_watched = 0
    db.commit()
    db.refresh(movie)
    return True