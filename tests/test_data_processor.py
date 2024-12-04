"""
Unit tests for the DataProcessor class.
Tests data processing functionality for movie ratings and movie information,
including CSV file handling and model validation.
"""
import pandas as pd
import pytest

from jarvis.data.processor import DataProcessor
from jarvis.schema.models import Movie, Rating


@pytest.fixture
def sample_data_directory(tmp_path):
    """
    Create a temporary directory with sample movie and rating data.

    Args:
        tmp_path: pytest fixture providing temporary directory path

    Returns:
        Path: Directory containing sample data files
    """
    # Create sample ratings data
    ratings_data = pd.DataFrame(
        {
            "userId": [1, 2],
            "movieId": [1, 2],
            "rating": [4.0, 5.0],
            "timestamp": [1400000000, 1500000000],
        }
    )

    # Create sample movies data
    movies_data = pd.DataFrame(
        {
            "movieId": [1, 2],
            "title": ["Finding Nimo", "Finding Asoom"],
            "genres": ["Action|Comedy", "Drama"],
        }
    )

    # Create directory and save files
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    ratings_data.to_csv(raw_dir / "ratings.csv", index=False)
    movies_data.to_csv(raw_dir / "movies.csv", index=False)

    return tmp_path


def test_rating_processor(sample_data_directory, monkeypatch):
    """
    Test the rating processing functionality.

    Verifies that ratings are correctly loaded and converted to Rating objects.
    """
    # Mock Settings
    monkeypatch.setattr(
        "jarvis.config.settings.RAW_DATA_DIR", sample_data_directory / "raw"
    )
    monkeypatch.setattr(
        "jarvis.config.settings.PROCESSED_DATA_DIR", sample_data_directory / "processed"
    )

    processor = DataProcessor()
    processed_ratings = list(processor.process_ratings())

    assert len(processed_ratings) == 2
    assert isinstance(processed_ratings[0], Rating)
    assert processed_ratings[0].user_id == 1
    assert processed_ratings[0].rating == 4.0


def test_movie_processor(sample_data_directory, monkeypatch):
    """
    Test the movie processing functionality.

    Verifies that movies are correctly loaded and converted to Movie objects,
    including proper genre splitting.
    """
    monkeypatch.setattr(
        "jarvis.config.settings.RAW_DATA_DIR", sample_data_directory / "raw"
    )
    monkeypatch.setattr(
        "jarvis.config.settings.PROCESSED_DATA_DIR", sample_data_directory / "processed"
    )

    processor = DataProcessor()
    movies = list(processor.process_movies())

    assert len(movies) == 2
    assert isinstance(movies[0], Movie)
    assert movies[0].title == "Finding Nimo"
    assert movies[0].genres == ["Action", "Comedy"]
