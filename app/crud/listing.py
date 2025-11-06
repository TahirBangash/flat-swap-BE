from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.listing import Listing
from app.schemas.listing import (
    UnitListingCreate,
    RoomListingCreate,
    UnitListingUpdate,
    RoomListingUpdate,
    ListingCreate
)


def get_listing(db: Session, listing_id: int) -> Optional[Listing]:
    return db.query(Listing).options(joinedload(Listing.user)).filter(Listing.id == listing_id).first()


def get_listings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    listing_type: Optional[str] = None,
    user_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rooms: Optional[int] = None,
    max_rooms: Optional[int] = None,
    min_bathrooms: Optional[int] = None,
    max_bathrooms: Optional[int] = None,
    max_distance: Optional[int] = None,
    furnished: Optional[bool] = None,
    gym_in_building: Optional[bool] = None,
    laundry_in_unit: Optional[bool] = None,
    laundry_in_building: Optional[bool] = None
) -> List[Listing]:
    query = db.query(Listing).options(joinedload(Listing.user))
    
    # Basic filters
    if listing_type:
        query = query.filter(Listing.listing_type == listing_type)
    
    if user_id:
        query = query.filter(Listing.user_id == user_id)
    
    # Price filters - check both unit_price and price_per_room
    if min_price is not None:
        query = query.filter(
            (Listing.unit_price >= min_price) | (Listing.price_per_room >= min_price)
        )
    
    if max_price is not None:
        query = query.filter(
            (Listing.unit_price <= max_price) | (Listing.price_per_room <= max_price)
        )
    
    # Room filters
    if min_rooms is not None:
        query = query.filter(Listing.num_rooms_available >= min_rooms)
    
    if max_rooms is not None:
        query = query.filter(Listing.num_rooms_available <= max_rooms)
    
    # Bathroom filters
    if min_bathrooms is not None:
        query = query.filter(Listing.num_bathrooms >= min_bathrooms)
    
    if max_bathrooms is not None:
        query = query.filter(Listing.num_bathrooms <= max_bathrooms)
    
    # Distance filter
    if max_distance is not None:
        query = query.filter(Listing.distance_to_university <= max_distance)
    
    # Amenity filters
    if furnished is not None:
        query = query.filter(Listing.furnished == furnished)
    
    if gym_in_building is not None:
        query = query.filter(Listing.gym_in_building == gym_in_building)
    
    if laundry_in_unit is not None:
        query = query.filter(Listing.laundry_in_unit == laundry_in_unit)
    
    if laundry_in_building is not None:
        query = query.filter(Listing.laundry_in_building == laundry_in_building)
    
    return query.offset(skip).limit(limit).all()


def get_user_listings(db: Session, user_id: int) -> List[Listing]:
    return db.query(Listing).options(joinedload(Listing.user)).filter(Listing.user_id == user_id).all()


def create_listing(db: Session, listing_data: ListingCreate, user_id: int) -> Listing:
    base_data = listing_data.model_dump(exclude={"listing_type", "unit_price", "total_ensuite", "total_shared_bathrooms", "price_per_room", "how_many_ensuite_rooms", "how_many_shared_bathrooms_in_apartment"})
    
    if isinstance(listing_data, UnitListingCreate):
        db_listing = Listing(
            user_id=user_id,
            listing_type="unit",
            unit_price=listing_data.unit_price,
            total_ensuite=listing_data.total_ensuite,
            total_shared_bathrooms=listing_data.total_shared_bathrooms,
            price_per_room=None,
            how_many_ensuite_rooms=None,
            how_many_shared_bathrooms_in_apartment=None,
            **base_data
        )
    elif isinstance(listing_data, RoomListingCreate):
        db_listing = Listing(
            user_id=user_id,
            listing_type="room",
            price_per_room=listing_data.price_per_room,
            how_many_ensuite_rooms=listing_data.how_many_ensuite_rooms,
            how_many_shared_bathrooms_in_apartment=listing_data.how_many_shared_bathrooms_in_apartment,
            unit_price=None,
            total_ensuite=None,
            total_shared_bathrooms=None,
            **base_data
        )
    else:
        raise ValueError(f"Unknown listing type: {type(listing_data)}")
    
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


def update_listing(
    db: Session,
    listing_id: int,
    listing_update: UnitListingUpdate | RoomListingUpdate
) -> Optional[Listing]:
    db_listing = get_listing(db, listing_id)
    if not db_listing:
        return None
    
    update_data = listing_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if hasattr(db_listing, field):
            setattr(db_listing, field, value)
    
    db.commit()
    db.refresh(db_listing)
    return db_listing


def delete_listing(db: Session, listing_id: int) -> bool:
    db_listing = get_listing(db, listing_id)
    if not db_listing:
        return False
    
    db.delete(db_listing)
    db.commit()
    return True

