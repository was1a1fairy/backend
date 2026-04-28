from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    genre: Mapped[str] = mapped_column(String(128))
    release_year: Mapped[int] = mapped_column(gt=1900, lt=2100)
    is_watched: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)