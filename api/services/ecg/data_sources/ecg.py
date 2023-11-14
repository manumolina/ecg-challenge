from uuid import uuid4
from core.database import database
from services.ecg.schemas.ecg import ECG, ECGLead
from services.ecg.exceptions import ECGErrorSavingData, ECGUnknownError
from sqlalchemy import exc


class ECGData:

    @staticmethod
    def insert(
        user_id: uuid4, ecg_lead_list: list[ECG]
    ) -> None:
        """Insert in the DB the ECG header and its signals.

        Args:
            user_id (uuid.uuid4)
            ecg_lead_list (list[ECG])
        """
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
    ) -> list:
        """Gets data from DB using information from query.

        Args:
            tables (list): tables involved in the query
            where (dict): filter to apply
            offset (int, optional): Defaults to 0.
            limit (int, optional): Defaults to 100.

        Returns:
            list: data extracted from DB
        """
        # tables allowed: ECG, ECGLead
        with database.session() as session:
            query = session.query(*tables).join(ECGLead)
            for key, value in where.items():
                query = query.filter(key == value)
            return query.offset(offset).limit(limit).all()
