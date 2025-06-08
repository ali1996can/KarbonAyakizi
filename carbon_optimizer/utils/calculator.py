import pandas as pd
from datetime import datetime
import os
import json
import csv

def log_to_csv(input_data, total_emission):
    os.makedirs("results", exist_ok=True)
    file_path = "results/usage_log.csv"
    file_exists = os.path.isfile(file_path)

    fieldnames = ["timestamp", "city", "beef", "chicken", "car", "electricity", "total_emission"]

    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        row = {
            "timestamp": datetime.now().isoformat(),
            "city": input_data.get("city", "Bilinmiyor"),
            "beef": input_data["beef"],
            "chicken": input_data["chicken"],
            "car": input_data["car"],
            "electricity": input_data["electricity"],
            "total_emission": total_emission
        }

        writer.writerow(row)

def load_emission_factors(city=None):
    base_dir = os.path.dirname(__file__)  # utils klasörünün yolu
    factors_path = os.path.join(base_dir, "factors.json")
    with open(factors_path, "r", encoding="utf-8") as f:
        all_factors = json.load(f)

    if city and city in all_factors:
        return all_factors[city]
    return all_factors  # şehir yoksa tüm faktörleri döndürebilir

def calculate_emission(data, emission_factors):
    total_emission = 0.0
    breakdown = {}
    for key, value in data.items():
        if key in emission_factors:
            emission = value * emission_factors[key]
            total_emission += emission
            breakdown[key] = (value, emission)  # value ve emission tuple olarak
    return total_emission, breakdown

