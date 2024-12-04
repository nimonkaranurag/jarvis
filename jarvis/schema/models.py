"""
Pydantic models for movie ratings and tags system.
This module defines the data models for handling movie ratings, movie information,
and user-generated tags.
"""
from datetime import datetime

from pydantic import BaseModel, Field


class Rating(BaseModel):
    """
    Represents a user's rating for a movie.

    Attributes:
        user_id (int): Unique identifier for the user
        movie_id (int): Unique identifier for the movie
        rating (float): User's rating from 0.5 to 5.0
        timestamp (datetime): When the rating was submitted
    """

    user_id: int = Field(..., gt=0)
    movie_id: int = Field(..., gt=0)
    rating: float = Field(..., ge=0.5, le=5.0)
    timestamp: datetime


class Movie(BaseModel):
    """
    Represents a movie in the system.

    Attributes:
        movie_id (int): Unique identifier for the movie
        title (str): Movie title
        genres (list[str]): List of genres associated with the movie
    """

    movie_id: int = Field(..., gt=0)
    title: str
    genres: list[str]


class Tag(BaseModel):
    """
    Represents a user-generated tag for a movie.

    Attributes:
        user_id (int): Unique identifier for the user
        movie_id (int): Unique identifier for the movie
        tag (str): The tag text
        timestamp (datetime): When the tag was created
    """

    user_id: int = Field(..., gt=0)
    movie_id: int = Field(..., gt=0)
    tag: str
    timestamp: datetime
