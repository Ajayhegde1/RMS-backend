# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
from dotenv import load_dotenv
from .config import DATABASE_URL
import os
import pymysql
pymysql.install_as_MySQLdb()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
SQLALCHEMY_DATABASE_URL = DATABASE_URL


if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
def create_tables():
    from .models import (
        RestaurantUser, Review,Restaurant, NFCDesign, 
        CustomizationRequest, GenerateQR, BaseDesign, FoodRecipeSteps,
        Cuisine, Vendor, Cart, Platform, RawMaterialCategory,RawMaterial, Food, FoodRawMaterial
    )
    Base.metadata.create_all(bind=engine)

