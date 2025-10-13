from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine(settings.database_url, pool_pre_ping=True)
sessionlocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
