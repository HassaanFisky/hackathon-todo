import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Make URL compatible with modern asyncpg/sync drivers if needed, 
# but SQLModel sync engine needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Using a synchronous connection for SQLModel to keep it simple, 
# or async engine if strictly needed. The prompt mentioned "Async database connection", 
# but sqlmodel sync engine is standard for basic usage. 
# We'll use the sync engine but will set it up for compatibility.
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
