#Handles database operations for the User entity.

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.security.hashing import hash_password
from app.security.hashing import verify_password



def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Find a user by email.
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user.
    """

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hash_password(user.password),  #It guarantees that no part of the application can accidentally save a plain-text password.
        phone=user.phone,
        country=user.country,
        currency=user.currency
    )
    
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ) -> User | None:

        user = get_user_by_email(
            db,
            email
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash
        ):
            return None

        return user

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user