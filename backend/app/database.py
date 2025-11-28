from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Create the database engine
engine = create_engine('postgresql://user:password@localhost/dbname')

# Create the session maker
Session = sessionmaker(bind=engine)

# Create the tables
Base.metadata.create_all(engine)
