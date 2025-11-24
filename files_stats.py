import os
import requests
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Token aus der .env lesen
ACCESS_TOKEN = os.getenv("ZENODO_TOKEN")

ZENODO_API = "https://zenodo.org/api/records"
COMMUNITY = "lory_phlu"  # Name der Community


def get_records(page=1):
    params = {
        "communities": COMMUNITY,
        "page": page,
        "size": 100,
    }

    # Token nur senden, wenn vorhanden
    if ACCESS_TOKEN:
        params["access_token"] = ACCESS_TOKEN

    return requests.get(ZENODO_API, params=params).json()


def sum_total_bytes():
    total_bytes = 0
    page = 1

    while True:
        data = get_records(page)
        hits = data.get("hits", {}).get("hits", [])

        if not hits:
            break

        for record in hits:
            files = record.get("files", [])
            for f in files:
                size = f.get("size", 0)
                total_bytes += size

        page += 1

    return total_bytes


if __name__ == "__main__":
    total = sum_total_bytes()
    print(f"Total size of all files in community '{COMMUNITY}': {total / 1e9:.3f} GB")
