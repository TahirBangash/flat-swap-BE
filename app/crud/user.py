from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Get a user by ID
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    if not email:
        return None
    return db.query(User).filter(User.email == email).first()


def get_user_by_auth0_id(db: Session, auth0_user_id: str) -> Optional[User]:
    """
    Get a user by Auth0 user ID (sub claim)
    """
    return db.query(User).filter(User.auth0_user_id == auth0_user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get a user by username
    """
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get list of users with pagination
    """
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Create a new user (manual creation - not used with Auth0)
    Note: With Auth0, users are created via get_or_create_user_from_auth0()
    """
    # Note: This function requires auth0_user_id but UserCreate doesn't have it
    # This function is kept for potential admin/manual user creation
    # For Auth0 users, use get_or_create_user_from_auth0() instead
    db_user = User(
        auth0_user_id=user_data.auth0_user_id if hasattr(user_data, 'auth0_user_id') else f"manual-{user_data.email}",
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        profile_picture_url=user_data.profile_picture_url,
        hashed_password=None,  # No password with Auth0
        is_active=user_data.is_active if user_data.is_active is not None else True,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data.pop("password")
    
    email = update_data.get("email") if "email" in update_data else db_user.email
    first_name = update_data.get("first_name") if "first_name" in update_data else db_user.first_name
    last_name = update_data.get("last_name") if "last_name" in update_data else db_user.last_name
    
    if email and first_name:
        update_data["profile_complete"] = True
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user
    """
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def get_or_create_user_from_auth0(
    db: Session,
    id_token_payload: Dict[str, Any]
) -> User:
    auth0_user_id = id_token_payload.get("sub")
    
    if not auth0_user_id:
        raise ValueError("ID token missing required claim: sub")
    
    email = id_token_payload.get("email")
    name = id_token_payload.get("name") or id_token_payload.get("nickname")
    picture = id_token_payload.get("picture")
    
    user = get_user_by_auth0_id(db, auth0_user_id)
    
    if user:
        update_data = {}
        
        if email and email != user.email:
            update_data["email"] = email
        
        if name and name.strip():
            name_parts = name.split(" ", 1)
            if len(name_parts) == 2:
                new_first = name_parts[0]
                new_last = name_parts[1]
            else:
                new_first = name_parts[0]
                new_last = None
            
            if new_first != user.first_name or new_last != user.last_name:
                update_data["first_name"] = new_first
                update_data["last_name"] = new_last
        
        if picture and picture != user.profile_picture_url:
            update_data["profile_picture_url"] = picture
        
        if email and name:
            update_data["profile_complete"] = True
        
        if update_data:
            for field, value in update_data.items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
        
        return user
    
    first_name = None
    last_name = None
    
    if name and name.strip():
        name_parts = name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else None
    
    profile_complete = bool(email and name)
    
    new_user = User(
        auth0_user_id=auth0_user_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
        profile_picture_url=picture,
        is_active=True,
        is_superuser=False,
        profile_complete=profile_complete
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

