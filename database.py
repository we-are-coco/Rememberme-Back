import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

SSL_CERT_PATH = os.path.join(os.getcwd(), "DigiCertGlobalRootCA.crt.pem")
SQLALCHEMY_DATABASE_URL = (
    "mysql+mysqldb://"
    f"{settings.database_username}:{settings.database_password}"
    f"@{settings.database_host}/{settings.database_name}"
    "?ssl_ca=" + SSL_CERT_PATH
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()