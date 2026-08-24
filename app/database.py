from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

def get_database_url():
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    secret_path = os.getenv("DB_PASSWORD_FILE", "/run/secrets/db_password")
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            password = f.read().strip()
    else:
        password = os.getenv("POSTGRES_PASSWORD", "1234")

    user = os.getenv("POSTGRES_USER", "Composer")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "latihan")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

SQLALCHEMY_DATABASE_URL = get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
