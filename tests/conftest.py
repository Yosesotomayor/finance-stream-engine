import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.models.db_models import TransactionDBModel
from src.database.connection import get_engine

engine = get_engine()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()  # Reverts any changes made during the test
    connection.close()