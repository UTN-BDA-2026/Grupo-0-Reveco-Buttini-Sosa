from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate):     #C
        user = User(
            name = user_create.name,
            surname = user_create.surname,
            username = user_create.username,
            email = user_create.email,  
            password = user_create.password #TODO: Hashear la contraseña
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int):            #R
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str):           #R
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str):     #R
        return self.db.query(User).filter(User.username == username).first()
    
    def update_user(self, user_id: int, user_update: UserCreate):  #U
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        user.name = user_update.name
        user.surname = user_update.surname
        user.username = user_update.username
        user.email = user_update.email
        user.password = user_update.password #TODO: Hashear la contraseña

        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int):         #D
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        self.db.delete(user)
        self.db.commit()
        return user