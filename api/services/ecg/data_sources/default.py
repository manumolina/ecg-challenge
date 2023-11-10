import uuid
from core.database import database
from services.ecg.schemas.ecg import ECG, ECGLead
from services.ecg.exceptions import ECGErrorSavingData, ECGUnknownError
from sqlalchemy import exc


class ECGData:

    @staticmethod
    def insert(
        user_id: uuid.uuid4, ecg_lead_list: list[ECG]
    ) -> None:
        with database.session() as session:
            try:
                # header
                new_ecg = ECG(**{"user": user_id})
                session.add(new_ecg)

                # detail
                for ecg_lead in ecg_lead_list:
                    session.add(ECGLead(**ecg_lead | {"ecg_id": new_ecg.id}))
                session.commit()
            except exc.IntegrityError:
                ECGErrorSavingData()
            except Exception as e:
                ECGUnknownError(e)

    @staticmethod
    def get(
        tables: list,
        where: dict,
        offset: int = 0,
        limit: int = 100
    ):
        # tables allowed: ECG, ECGLead
        with database.session() as session:
            query = session.query(*tables).join(ECGLead)
            for key, value in where.items():
                query = query.filter(key == value)
            return query.offset(offset).limit(limit).all()
