from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "password"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "ssss"

DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# DATABASE_USERNAME = "root"
# DATABASE_PASSWORD = "password"
# DATABASE_HOST = "localhost"
# DATABASE_PORT = "3306"
# DATABASE_NAME = "brsr"

# DATABASE_URL = (
#     f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
# )

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(bind=engine)


# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)