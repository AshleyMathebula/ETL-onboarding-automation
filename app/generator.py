from pathlib import Path
from datetime import datetime
import re


OUTPUT_DIR = Path("outputs")


def safe_filename(name):
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9]+", "_", name)
    return name.strip("_") or "unknown_client"


def generate_output_files_by_client(records):
    OUTPUT_DIR.mkdir(exist_ok=True)

    grouped_records = {}

    for record in records:
        client_name = record["client_name"]
        grouped_records.setdefault(client_name, []).append(record)

    generated_files = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for client_name, client_records in grouped_records.items():
        filename = f"{safe_filename(client_name)}_{timestamp}.txt"
        file_path = OUTPUT_DIR / filename

        with open(file_path, "w", encoding="utf-8") as file:
            for record in client_records:
                file.write(f"?,?,{record['whitelist_number']}\n")

        generated_files.append(file_path)

    return generated_files