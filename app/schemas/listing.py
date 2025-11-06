from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing import Optional, List, Literal
from datetime import date, datetime


class ListingBase(BaseModel):
    address: str
    num_rooms_available: int
    total_rooms: int
    num_bathrooms: int
    furnished: bool
    ensuite: int
    start_date: date
    end_date: date
    
    distance_to_university: Optional[int] = None
    gym_in_building: Optional[bool] = None
    laundry_in_unit: Optional[bool] = None
    laundry_in_building: Optional[bool] = None
    utilities_included: Optional[str] = None
    building_name: Optional[str] = None
    images: Optional[List[str]] = None


class UnitListingCreate(ListingBase):
    listing_type: Literal["unit"] = "unit"
    unit_price: float = Field(..., description="Total price for entire unit")
    total_ensuite: int = Field(..., description="Total ensuite bathrooms in unit")
    total_shared_bathrooms: int = Field(..., description="Total shared bathrooms in unit")


class RoomListingCreate(ListingBase):
    listing_type: Literal["room"] = "room"
    price_per_room: float = Field(..., description="Price per room")
    how_many_ensuite_rooms: int = Field(..., description="How many ensuite rooms available")
    how_many_shared_bathrooms_in_apartment: int = Field(..., description="How many shared bathrooms in apartment")


class UnitListingUpdate(BaseModel):
    address: Optional[str] = None
    num_rooms_available: Optional[int] = None
    total_rooms: Optional[int] = None
    num_bathrooms: Optional[int] = None
    furnished: Optional[bool] = None
    ensuite: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    distance_to_university: Optional[int] = None
    gym_in_building: Optional[bool] = None
    laundry_in_unit: Optional[bool] = None
    laundry_in_building: Optional[bool] = None
    utilities_included: Optional[str] = None
    building_name: Optional[str] = None
    images: Optional[List[str]] = None
    unit_price: Optional[float] = None
    total_ensuite: Optional[int] = None
    total_shared_bathrooms: Optional[int] = None


class RoomListingUpdate(BaseModel):
    address: Optional[str] = None
    num_rooms_available: Optional[int] = None
    total_rooms: Optional[int] = None
    num_bathrooms: Optional[int] = None
    furnished: Optional[bool] = None
    ensuite: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    distance_to_university: Optional[int] = None
    gym_in_building: Optional[bool] = None
    laundry_in_unit: Optional[bool] = None
    laundry_in_building: Optional[bool] = None
    utilities_included: Optional[str] = None
    building_name: Optional[str] = None
    images: Optional[List[str]] = None
    price_per_room: Optional[float] = None
    how_many_ensuite_rooms: Optional[int] = None
    how_many_shared_bathrooms_in_apartment: Optional[int] = None


class ListingUserInfo(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    
    @computed_field
    @property
    def full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return ""
    
    model_config = ConfigDict(from_attributes=True)


class UnitListing(ListingBase):
    id: int
    listing_type: Literal["unit"] = "unit"
    unit_price: float
    total_ensuite: int
    total_shared_bathrooms: int
    user_id: int
    user: ListingUserInfo
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class RoomListing(ListingBase):
    id: int
    listing_type: Literal["room"] = "room"
    price_per_room: float
    how_many_ensuite_rooms: int
    how_many_shared_bathrooms_in_apartment: int
    user_id: int
    user: ListingUserInfo
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


ListingCreate = UnitListingCreate | RoomListingCreate
Listing = UnitListing | RoomListing

