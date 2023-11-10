import uuid
from datetime import datetime

from services.user.schemas.user import User, UserImport
from services.user.data_sources.default import UserData


class UserLogic:

    def new(self, user: UserImport):
        return UserData.insert(User(**user.__dict__))
