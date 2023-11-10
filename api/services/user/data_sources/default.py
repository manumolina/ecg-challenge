from core.database import database
from services.user.schemas.user import User


class UserData:

    @staticmethod
    def insert(user: User):
        with database.session() as session:
            session.add(user)
            session.commit()
        return True
