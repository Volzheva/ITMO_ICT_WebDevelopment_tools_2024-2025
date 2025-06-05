from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
load_dotenv()

#db_url="postgresql://postgres:postgres@db/hackathon_db"
db_url="postgresql://postgres:postgres@localhost/hackathon_db"

engine = create_engine(db_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session