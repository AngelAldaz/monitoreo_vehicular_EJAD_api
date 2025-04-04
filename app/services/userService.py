from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas.usersSchema import UserCreate, UserOut, TokenData, UserUpdate
from app.repositories.userRepository import UserRepository
from app.models.usersModel import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

class UserService:
  def __init__(self, user_repo: UserRepository) -> None:
    self.repo = user_repo
        
  def create_user(self, user: UserCreate) -> UserOut:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
      first_name=user.first_name,
      last_name=user.last_name,
      email=user.email,
      password=hashed_password,
      id_role_fk=2
    )
    created_user = self.repo.create_user(db_user)
    return UserOut(
      id_usuario=created_user.id_usuario,
      first_name=created_user.first_name,
      last_name=created_user.last_name,
      email=created_user.email,
      id_role_fk=created_user.id_role_fk,
      id_vehicle_fk=db_user.id_vehicle_fk
    
    )
    
  def get_user_by_id(self, user_id: int) -> Optional[UserOut]:
    db_user = self.repo.get_user_by_id(user_id)
    if db_user:
      return UserOut(
        id_usuario=db_user.id_usuario,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        email=db_user.email,
        id_role_fk=db_user.id_role_fk,
        id_vehicle_fk=db_user.id_vehicle_fk
      )
  
  def get_all_users(self) -> list[UserOut]:
    db_users = self.repo.get_all_users()
    return [
      UserOut(
        id_usuario=user.id_usuario,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        id_role_fk=user.id_role_fk,
        id_vehicle_fk=user.id_vehicle_fk
      ) for user in db_users
    ]
  
  def update_user(self, user_id: int, user: UserUpdate) -> Optional[UserOut]:
    db_user = self.repo.get_user_by_id(user_id)
    if db_user:
      if user.first_name is not None:
        db_user.first_name = user.first_name
      if user.last_name is not None:
        db_user.last_name = user.last_name
      if user.email is not None:
        db_user.email = user.email
      if user.password is not None:
        db_user.password = pwd_context.hash(user.password)
      if user.id_role_fk is not None:
        db_user.id_role_fk = user.id_role_fk
      if user.id_vehicle_fk is not None:
        db_user.id_vehicle_fk = user.id_vehicle_fk
      updated_user = self.repo.update_user(db_user)
      return UserOut(
        id_usuario=updated_user.id_usuario,
        first_name=updated_user.first_name,
        last_name=updated_user.last_name,
        email=updated_user.email,
        id_role_fk=updated_user.id_role_fk,
        id_vehicle_fk=updated_user.id_vehicle_fk
      )
  
  def delete_user(self, user_id: int) -> bool:
    db_user = self.repo.get_user_by_id(user_id)
    if db_user:
      return self.repo.delete_user(db_user)
    return False
  
  def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.repo.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.password):
            return None
        return user
      
  def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
      expire = datetime.utcnow() + expires_delta
    else:
      expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
  def get_current_user(self, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload.get("sub")
      user_id: int = payload.get("user_id")
      if email is None or user_id is None:
        raise credentials_exception
      token_data = TokenData(email=email, user_id=user_id)
    except JWTError:
      raise credentials_exception
    
    user = self.repo.get_user_by_id(token_data.user_id)
    if user is None:
      raise credentials_exception
    return user