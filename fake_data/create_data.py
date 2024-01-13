import random
import json

NUM_ROWS = 1000000

def generate_random_ecg(num_rows: int):
    default_name = "test_"
    path = f"fake_data_{NUM_ROWS}.json"
    with open(path, 'w') as outfile:
        ecg_fake_data = []
        for i in range(num_rows):
            tmp_name = default_name + str(i)
            tmp_total_samples = random.randint(1, 100)
            tmp_signal = [random.randint(-10, 10) for _ in range(tmp_total_samples)]
            ecg_fake_data.append({
                "name": tmp_name, "total_samples": tmp_total_samples, "signal": tmp_signal
            })
        json.dump(ecg_fake_data, outfile, indent=4)

if __name__ == "__main__":
    generate_random_ecg(NUM_ROWS)
