"""
Script to create database tables
Run this once to initialize your database
"""
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.listing import Listing

print("Creating database tables")
Base.metadata.create_all(bind=engine)
print("tables created")


