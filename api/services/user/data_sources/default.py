from sqlalchemy import exc
from passlib.context import CryptContext

from core.database import database
from services.user.exceptions import UserErrorSavingData, UserUnknownError
from services.user.schemas.user import User


class UserData:

    @staticmethod
    def insert(user: User) -> None:
        with database.session() as session:
            try:
                session.add(user)
                session.commit()
            except exc.IntegrityError:
                UserErrorSavingData()
            except Exception as e:
                UserUnknownError(e)

    @staticmethod
    def get(
        where: dict,
        offset: int = 0,
        limit: int = 100
    ):
        # tables allowed: User
        with database.session() as session:
            query = session.query(User)
            for key, value in where.items():
                query = query.filter(key == value)
            return query.offset(offset).limit(limit).all()

    @staticmethod
    def validate_password_by_email(email: str, password: str):
        # tables allowed: User
        with database.session() as session:
            query = session.query(User)
            query = query.where(User.email == email)
            query = query.limit(1)
            results = session.exec(query)
            for r in results:
                user = r[0]
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                if not pwd_context.verify(
                    password, user.__dict__["password"]
                ):
                    return False
                return user.__dict__

    @staticmethod
    def validate_user_has_role_by_email(email: str, role: int):
        # tables allowed: User
        with database.session() as session:
            query = session.query(User)
            query = query.where(User.email == email)
            query = query.where(User.role == role)
            query = query.limit(1)
            results = session.exec(query).all()
            return results
