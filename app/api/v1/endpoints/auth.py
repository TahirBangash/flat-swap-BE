from fastapi import APIRouter, Depends
from app.schemas.user import User
from app.api.deps import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Get current logged-in user information from Auth0 token
    """
    return current_user


#same function as above 
@router.get("/verify", response_model=User)
async def verify_token(
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Verify Auth0 token and return user info
    This endpoint can be used to check if a token is valid
    """
    return current_user
