"""
Command Line Interface for Jarvis application.
Provides commands for database setup and management using MovieLens dataset.
Handles progress reporting and error logging.
"""
import typer
from loguru import logger
from rich.console import Console
from rich.progress import Progress

from jarvis.data.processor import DataProcessor
from jarvis.database.neo4j_manager import Neo4jManager

app = typer.Typer()
console = Console()


@app.command()
def setup_database():
    """Initialize and set-up Neo4j database with Kaggle's MovieLens dataset."""
    try:
        processor = DataProcessor()
        db_manager = Neo4jManager()

        with Progress() as progress:
            # Process and load movies
            load_movies = progress.add_task("Loading movies...", total=None)
            with db_manager.get_session() as session:  # Add this method to Neo4jManager
                for movie in processor.process_movies():
                    db_manager.create_movie(movie, session)
                    progress.update(load_movies, advance=1)

            # Process and load ratings
            load_ratings = progress.add_task("Loading ratings...", total=None)
            with db_manager.get_session() as session:  # Add this method to Neo4jManager
                for rating in processor.process_ratings():
                    db_manager.create_rating(rating, session)
                    progress.update(load_ratings, advance=1)

        console.print("Database set-up finished successfully!", style="green")
    except Exception as e:
        logger.error(f"Failed to set-up database, Error: {e}")
        raise typer.Exit(1)
    finally:
        db_manager.close()


if __name__ == "__main__":
    app()
