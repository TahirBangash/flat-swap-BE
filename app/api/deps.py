from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from app.core.config import settings
from app.core.security import verify_auth0_token, verify_id_token
from app.db.session import get_db
from app.crud import user_crud
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    x_id_token: Optional[str] = Header(None, alias="X-ID-Token")
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    access_token = credentials.credentials
    
    try:
        payload = verify_auth0_token(access_token)
        auth0_user_id = payload.get("sub")
        
        if not auth0_user_id:
            raise credentials_exception
        
        user = user_crud.get_user_by_auth0_id(db, auth0_user_id)
        
        if not user:
            if not x_id_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID token required for new user registration. Send X-ID-Token header."
                )
            
            id_payload = verify_id_token(x_id_token)
            
            if id_payload.get("sub") != auth0_user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="ID token sub does not match access token sub"
                )
            
            user = user_crud.get_or_create_user_from_auth0(
                db=db,
                id_token_payload=id_payload
            )
        
        return user
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user (not disabled)
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

