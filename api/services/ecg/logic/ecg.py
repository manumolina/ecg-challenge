import uuid
from fastapi import Request
from services.ecg.schemas.ecg import (
    ECG, ECGLead, ECGImportList, ECGOutput
)
from api.services.ecg.data_sources.ecg import ECGData
from api.services.user.logic.user import UserLogic


class ECGLogic:
    def __init__(self, request: Request) -> None:
        self.user_id = UserLogic().get_user_id_from_request(request)

    # ------------- #
    # Basic methods
    # ------------- #
    def load(
        self, ecg_list: ECGImportList
    ) -> dict:
        """This method:
        * Analize total samples and signals are equal
        * Execute algorithm to calculate nº of zeros in signals
        * Save info in DB

        Args:
            ecg_list (ECGImportList): list of ecgs to saved

        Returns:
            dict: result of the operation
        """
        valid_ecgs = []
        invalid_ecgs = []
        for ecg_object in ecg_list:
            ecg = ecg_object.__dict__
            if "total_samples" in ecg.keys() \
               and (ecg["total_samples"] <= 0
               or ecg["total_samples"] and ecg["total_samples"] != len(ecg["signal"])):
                invalid_ecgs.append(ecg)
                continue

            if not ecg["total_samples"]:
                ecg["total_samples"] = len(ecg["signal"])

            ecg["t_cross_zero"] = self.total_number_crossing_signal(
                ecg["signal"], 0
            )
            valid_ecgs.append(ecg)

        return self.save(
            self.user_id, valid_ecgs, invalid_ecgs
        )

    @staticmethod
    def save(
        user_id: uuid.uuid4,
        valid_ecgs: list[dict],
        invalid_ecgs: list[dict]
    ) -> dict:
        """Save valid ecgs in the DB.
        Returns a dictionary with information
        about the result of the operation.

        Args:
            user_id (uuid.uuid4)
            valid_ecgs (list): contains valid ECG objects
            invalid_ecgs (list): contains invalid ECG objects

        Returns:
            dict: result of the operation
        """
        # save only if all ecgs are valid
        inserted = 0
        if not invalid_ecgs:
            inserted = len(valid_ecgs)
            ECGData.insert(user_id, valid_ecgs)

        return {
            "inserted": inserted,
            "valid": len(valid_ecgs),
            "invalid": {
                "total": len(invalid_ecgs),
                "data": invalid_ecgs
            }
        }

    def get_user_ecgs_from_request(self) -> list[dict]:
        """Returns a list with the user ECGs found in DB

        Args:
            request (Request)

        Returns:
            list[ECGOutput]: only allowed fields to be returned
        """
        result = ECGData.get(
            tables=[ECG, ECGLead],
            where={
                getattr(ECG, "user"): uuid.UUID(str(self.user_id))
            },
        )
        return [
            ECGOutput(**ecg[1].__dict__) for ecg in result
        ]

    def get_all_ecgs(self):
        pass

    def get_single_ecg(self):
        pass

    # ----------- #
    # Util methods
    # ----------- #
    @staticmethod
    def total_number_crossing_signal(
        signal: list, to_find: int = 0
    ) -> int:
        """Returns the total number of occurrences found in the signal.

        Args:
            signal (list): list of integers
            to_find (int, optional): number to found in the list.
                                     defaults to 0.

        Returns:
            int: number of occurrences
        """
        return signal.count(to_find)
