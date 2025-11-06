from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class User(Base):
    """
    SQLAlchemy User Model
    
    This represents the users table in the database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    auth0_user_id = Column(String, unique=True, index=True, nullable=False)  # Auth0 sub claim
    email = Column(String, unique=True, index=True, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    
    # Profile picture URL or path
    profile_picture_url = Column(String, nullable=True)
    
    # User status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    profile_complete = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    listings = relationship("Listing", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, firstname={self.first_name}, lastname={self.last_name})>"

