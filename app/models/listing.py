from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    listing_type = Column(String, nullable=False, index=True)
    
    user = relationship("User", back_populates="listings")
    
    address = Column(String, nullable=False)
    num_rooms_available = Column(Integer, nullable=False)
    total_rooms = Column(Integer, nullable=False)
    num_bathrooms = Column(Integer, nullable=False)
    furnished = Column(Boolean, nullable=False)
    ensuite = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    distance_to_university = Column(Integer, nullable=True)
    gym_in_building = Column(Boolean, nullable=True)
    laundry_in_unit = Column(Boolean, nullable=True)
    laundry_in_building = Column(Boolean, nullable=True)
    utilities_included = Column(String, nullable=True)
    building_name = Column(String, nullable=True)
    images = Column(JSON, nullable=True)
    
    unit_price = Column(Float, nullable=True)
    total_ensuite = Column(Integer, nullable=True)
    total_shared_bathrooms = Column(Integer, nullable=True)
    
    price_per_room = Column(Float, nullable=True)
    how_many_ensuite_rooms = Column(Integer, nullable=True)
    how_many_shared_bathrooms_in_apartment = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Listing(id={self.id}, type={self.listing_type}, address={self.address})>"

