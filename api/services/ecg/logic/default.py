from services.ecg.schemas.default import ECGImportList
from services.ecg.data_sources.default import ECGData

class ECGLogic:
    @staticmethod
    def load(ecg_list: ECGImportList):
        """
        * Analize content 
        (not necessary, previously checked)
        * Execute algorithm
        * Save info in DB
        """
        invalid_ecgs = []
        for ecg_object in ecg_list:
            ecg = ecg_object.__dict__
            if "total_samples" in ecg.keys() \
               and ecg["total_samples"] \
               and ecg["total_samples"] != len(ecg["signal"]):
                invalid_ecgs.append(ecg)
                continue
            ECGData.insert(ecg)
            print(ecg)
        print("Invalid: ", invalid_ecgs)
