from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Union

from app.db.session import get_db
from app.schemas.listing import (
    UnitListing,
    RoomListing,
    UnitListingCreate,
    RoomListingCreate,
    UnitListingUpdate,
    RoomListingUpdate,
    Listing
)
from app.crud import listing_crud
from app.api.deps import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter()


@router.post("", response_model=Union[UnitListing, RoomListing], status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_data: Union[UnitListingCreate, RoomListingCreate],
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    listing = listing_crud.create_listing(db, listing_data, current_user.id)
    return listing


@router.get("", response_model=List[Union[UnitListing, RoomListing]])
async def get_listings(
    skip: int = 0,
    limit: int = 100,
    listing_type: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get all listings (public endpoint - no authentication required)
    """
    if listing_type and listing_type not in ["unit", "room"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="listing_type must be 'unit' or 'room'"
        )
    
    listings = listing_crud.get_listings(
        db,
        skip=skip,
        limit=limit,
        listing_type=listing_type,
        user_id=user_id
    )
    return listings


@router.get("/my-listings", response_model=List[Union[UnitListing, RoomListing]])
async def get_my_listings(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    listings = listing_crud.get_user_listings(db, current_user.id)
    return listings


@router.get("/{listing_id}", response_model=Union[UnitListing, RoomListing])
async def get_listing_by_id(
    listing_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific listing by ID (public endpoint - no authentication required)
    """
    listing = listing_crud.get_listing(db, listing_id)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    return listing


@router.put("/{listing_id}", response_model=Union[UnitListing, RoomListing])
async def update_listing(
    listing_id: int,
    listing_update: Union[UnitListingUpdate, RoomListingUpdate],
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    listing = listing_crud.get_listing(db, listing_id)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    if listing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this listing"
        )
    
    updated_listing = listing_crud.update_listing(db, listing_id, listing_update)
    if not updated_listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    return updated_listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    listing = listing_crud.get_listing(db, listing_id)
    if not listing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    if listing.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this listing"
        )
    
    success = listing_crud.delete_listing(db, listing_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Listing not found"
        )
    
    return None

