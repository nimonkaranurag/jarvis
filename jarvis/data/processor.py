"""
Data processor module for handling movie ratings and movie data.
Provides functionality to process raw data files and convert them into structured
model instances for the application.
"""
from pathlib import Path
from typing import Iterator

import pandas as pd
from loguru import logger

from jarvis.config import settings
from jarvis.schema.models import Movie, Rating


class DataProcessor:
    """
    Processes raw movie and rating data files into structured model instances.

    Handles reading CSV files, data validation, and conversion into Pydantic models.
    Supports batch processing for large datasets.
    """

    def __init__(self):
        """Initialize processor with configured data directories."""
        self.raw_data_dir = settings.RAW_DATA_DIR
        self.processed_data_dir = settings.PROCESSED_DATA_DIR
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create necessary data directories if they don't exist."""
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)

    def process_ratings(self) -> Iterator[Rating]:
        """
        Process ratings data in batches and yield Rating model instances.

        Returns:
            Iterator[Rating]: Stream of validated Rating objects

        Raises:
            FileNotFoundError: If ratings file doesn't exist
        """
        ratings_path = self.raw_data_dir / settings.RATINGS_FILE
        if not ratings_path.exists():
            raise FileNotFoundError(f"File not found at {ratings_path}")

        logger.info(f"Processing ratings from {ratings_path}")
        for chunk in pd.read_csv(ratings_path, chunksize=settings.BATCH_SIZE):
            # Convert timestamp to datetime
            chunk["timestamp"] = pd.to_datetime(chunk["timestamp"], unit="s")
            # Validate and yield Rating objects
            for row in chunk.itertuples():
                try:
                    rating = Rating(
                        user_id=row.userId,
                        movie_id=row.movieId,
                        rating=row.rating,
                        timestamp=row.timestamp,
                    )
                    yield rating
                except (ValueError, AttributeError) as e:
                    logger.error(f"Error processing rating: {row}, Error: {e}")

    def process_movies(self) -> Iterator[Movie]:
        """
        Process movies data and yield Movie model instances.

        Returns:
            Iterator[Movie]: Stream of validated Movie objects

        Raises:
            FileNotFoundError: If movies file doesn't exist
        """
        movies_path = self.raw_data_dir / settings.MOVIES_FILE
        if not movies_path.exists():
            raise FileNotFoundError(f"File not found at {movies_path}")

        logger.info(f"Processing movies from {movies_path}")
        movies_df = pd.read_csv(movies_path)

        for row in movies_df.itertuples():
            try:
                genres = (
                    row.genres.split("|") if row.genres != "(no genres listed)" else []
                )
                movie = Movie(movie_id=row.movieId, title=row.title, genres=genres)
                yield movie
            except (ValueError, AttributeError) as e:
                logger.error(f"Error processing movie: {row}, Error: {e}")
