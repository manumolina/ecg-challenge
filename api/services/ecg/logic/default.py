import uuid
from datetime import datetime

from services.ecg.schemas.ecg import ECG, ECGImportList
from services.ecg.data_sources.default import ECGData


class ECGLogic:

    def load(
        self, user_id: uuid.uuid4, ecg_list: ECGImportList
    ) -> dict:
        """This method:
        * Analize total samples and signals are equal
        * Execute algorithm to calculate nº of zeros in signals
        * Save info in DB

        Args:
            user_id (uuid.uuid4)
            ecg_list (ECGImportList): list of ecgs to saved

        Returns:
            dict: result of the operation
        """
        valid_ecgs = []
        invalid_ecgs = []
        for ecg_object in ecg_list:
            ecg = ecg_object.__dict__
            if "total_samples" in ecg.keys() \
               and ecg["total_samples"] \
               and ecg["total_samples"] != len(ecg["signal"]):
                invalid_ecgs.append(ecg)
                continue

            if not ecg["total_samples"]:
                ecg["total_samples"] = len(ecg["signal"])

            ecg["t_cross_zero"] = self.total_zeros_crossing_signal(
                ecg["signal"]
            )
            valid_ecgs.append(ecg)

        return self.save(
            user_id, valid_ecgs, invalid_ecgs
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

    @staticmethod
    def total_zeros_crossing_signal(signal: list):
        return signal.count(0)
