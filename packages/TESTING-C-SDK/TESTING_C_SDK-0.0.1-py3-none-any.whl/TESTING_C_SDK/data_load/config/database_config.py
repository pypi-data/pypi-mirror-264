
from sqlalchemy import create_engine,URL
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from rich.console import Console
console = Console()
from sqlalchemy.orm import sessionmaker

DB_PORT=5555
DB_PASSWORD="Admin@12345$"
DB_USER="postgres"
DB_NAME="postgres-development"
DB_HOST="20.193.133.240"

connection_string = URL.create("postgresql+psycopg2",username=DB_USER,password=DB_PASSWORD,
    host=DB_HOST,database=DB_NAME,port=DB_PORT)


base_ip = DB_HOST
engine = create_engine(connection_string,pool_size=1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





def recreate_database():
    Base.metadata.create_all(engine)