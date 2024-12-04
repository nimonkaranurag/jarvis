"""
Neo4j database manager for the Jarvis application.
Handles database connections, schema setup, and CRUD operations
for movies and ratings data.
"""
from neo4j import GraphDatabase, Session

from jarvis.config import settings
from jarvis.schema.models import Movie, Rating


class Neo4jManager:
    """
    Manages Neo4j database operations for the MovieLens dataset.

    Handles database connection, schema setup, and data operations
    for movies, users, ratings, and genres.
    """

    def __init__(self):
        """Initialize Neo4j connection and setup schema."""
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        self._setup_schema()
        self.batch_size = settings.BATCH_SIZE

    def get_session(self) -> Session:
        """
        Create a new database session.

        Returns:
            Session: A new Neo4j session
        """
        return self._driver.session()

    def _setup_schema(self) -> None:
        """Set up Neo4j schema with constraints and indexes."""
        with self.get_session() as session:
            # Create constraints
            session.run(
                """
                CREATE CONSTRAINT user_id IF NOT EXISTS
                FOR (u:User) REQUIRE u.id IS UNIQUE
                """
            )
            session.run(
                """
                CREATE CONSTRAINT movie_id IF NOT EXISTS
                FOR (m:Movie) REQUIRE m.id IS UNIQUE
                """
            )
            # Create indexes
            session.run(
                """
                CREATE INDEX movie_title IF NOT EXISTS
                FOR (m:Movie) ON (m.title)
                """
            )

    def create_movie(self, movies: list[Movie], session: Session) -> None:
        """
        Create movie nodes and their genre relationships.

        Args:
            movies: List of Movie objects to create
            session: Active Neo4j session
        """
        query = """
        UNWIND $movies as movie
        MERGE (m:Movie {id: movie.movie_id})
        SET m.title = movie.title
        WITH m, movie
        UNWIND movie.genres as genre
        MERGE(g:Genre {name: genre})
        MERGE (m)-[:HAS_GENRE]->(g)
        """
        session.run(
            query,
            movies=[
                {
                    "movie_id": movie.movie_id,
                    "title": movie.title,
                    "genres": movie.genres,
                }
                for movie in movies
            ],
        )

    def create_rating(self, ratings: list[Rating], session: Session) -> None:
        """
        Create rating relationships between users and movies.

        Args:
            ratings: List of Rating objects to create
            session: Active Neo4j session
        """
        query = """
        UNWIND $ratings as rating
        MERGE (u:User {id: rating.user_id})
        MERGE (m:Movie {id: rating.movie_id})
        CREATE (u)-[r:RATED {rating: rating.rating, timestamp: datetime(rating.timestamp)}]->(m)
        """
        session.run(
            query,
            ratings=[
                {
                    "user_id": rating.user_id,
                    "movie_id": rating.movie_id,
                    "rating": rating.rating,
                    "timestamp": rating.timestamp.isoformat(),
                }
                for rating in ratings
            ],
        )

    def close(self) -> None:
        """Close the Neo4j driver connection."""
        self._driver.close()
