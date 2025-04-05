from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List
from sqlalchemy.orm import Session
from app.schemas.usersSchema import UserCreate, UserOut, UserLogin, Token
from app.services.userService import UserService
from app.repositories.userRepository import UserRepository
from app.database import get_db
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The created user"
)
async def create_user(
    user_data: UserCreate = Body(...),
    service: UserService = Depends(get_user_service)
):
    """
    Create a new user with the following details:
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **email**: User's email (must be unique)
    - **password**: User's password
    - **id_role_fk**: Role ID (foreign key)
    - **id_vehicle_fk**: (Optional) Vehicle ID (foreign key)
    """
    existing_user = service.repo.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return service.create_user(user_data)

@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Get a user by ID",
    responses={404: {"description": "User not found"}}
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """
    Get details of a specific user by their ID.
    """
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get(
    "/",
    response_model=List[UserOut],
    summary="Get all users"
)
async def list_users(
    service: UserService = Depends(get_user_service)
):
    """
    Retrieve a list of all registered users.
    """
    return service.get_all_users()

@router.put(
    "/{user_id}",
    response_model=UserOut,
    summary="Update a user",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"}
    }
)
async def update_user(
    user_id: int,
    user_data: UserCreate = Body(...),
    service: UserService = Depends(get_user_service)
):
    """
    Update an existing user's information.
    """
    updated_user = service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """
    Delete a specific user by their ID.
    """
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None

@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user",
    responses={
        200: {"description": "Authentication successful"},
        401: {"description": "Invalid credentials"}
    }
)
async def login(
    user_data: UserLogin = Body(...),
    service: UserService = Depends(get_user_service)
):
    """
    Authenticate a user with email and password.
    Returns a JWT token for authorized requests.
    """
    user = service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token}

# Ejemplo de ruta protegida
# @router.get("/me/", response_model=UserOut)
# async def read_users_me(
#     current_user: User = Depends(get_user_service().get_current_user)
# ):
#     """
#     Get current user details (protected route).
#     """
#     return current_user