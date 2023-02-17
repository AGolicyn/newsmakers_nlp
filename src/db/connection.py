from loguru import logger
from src.db.session import SessionLocal

class DatabaseSession:
    def __enter__(self):
        self.db = SessionLocal()
        logger.debug("Database session opened")
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        logger.debug("Database session closed")


