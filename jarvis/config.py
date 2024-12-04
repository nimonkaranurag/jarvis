"""
Configuration settings for the Jarvis application.
Handles environment variables, file paths, and database connection settings
using Pydantic's BaseSettings.
"""
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and configuration.

    Attributes:
        PROJECT_ROOT: Root directory of the project
        DATA_DIR: Directory for all data files
        RAW_DATA_DIR: Directory for raw input files
        PROCESSED_DATA_DIR: Directory for processed output files
        NEO4J_URI: Connection URI for Neo4j database
        NEO4J_USER: Neo4j database username
        NEO4J_PASSWORD: Neo4j database password
        RATINGS_FILE: Filename for ratings data
        MOVIES_FILE: Filename for movies data
        TAGS_FILE: Filename for tags data
        BATCH_SIZE: Number of records to process in each batch
    """

    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = PROJECT_ROOT / "raw"
    PROCESSED_DATA_DIR: Path = PROJECT_ROOT / "processed"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str
    RATINGS_FILE: str = "ratings.csv"
    MOVIES_FILE: str = "movies.csv"
    TAGS_FILE: str = "tags.csv"
    BATCH_SIZE: int = 10000

    class Config:
        """Pydantic configuration class for environment variable loading."""

        env_file = ".env"


settings = Settings()
