from sqlalchemy.orm import Session
from app.models.usersModel import User

class UserRepository:
  def __init__(self, db: Session) -> None:
    self.db = db
      
  def create_user(self, user: User) -> User:
    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)
    return user
  
  def get_user_by_id(self, user_id: int) -> User:
    return self.db.query(User).filter(User.id_usuario == user_id).first()
  
  def get_user_by_email(self, email: str) -> User:
    return self.db.query(User).filter(User.email == email).first()
  
  def get_all_users(self) -> list[User]:
    return self.db.query(User).all()
  
  def update_user(self, user: User) -> User:
    self.db.merge(user)
    self.db.commit()
    self.db.refresh(user)
    return user
  
  def delete_user(self, user: User) -> bool:
    self.db.delete(user)
    self.db.commit()
    return True