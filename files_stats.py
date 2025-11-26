import os
import argparse
import requests
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Token aus der .env lesen
ACCESS_TOKEN = os.getenv("ZENODO_TOKEN")

# Erstelle den ArgumentParser
parser = argparse.ArgumentParser(description='Check file size of a Zenodo Community via REST-API', usage="py files_stats.py --community {YOUR_COMMUNITY}")
# Füge das Argument 'shoulder' hinzu
parser.add_argument('--community', '-c', required=True, help='Your Zenodo-Community', )
# Parse die Argumente
args = parser.parse_args()


ZENODO_API = "https://zenodo.org/api/records"
# Name der Community festlegen
COMMUNITY = args.community  
page = 1
total_bytes = 0
# API-Doku: mit token max 100 pro Seite, ohne token / wenn instabil: 25
size = "100" 


headers = {}
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

params = {
        "communities": COMMUNITY,
        "size": size,
    }


def getRecords():
    r = requests.get(f"{ZENODO_API}", params=params, headers=headers)
    print("Status:", r.status_code)
    print("Headers:", r.headers)
    print("Text:", r.text[:500])
    return r.json()

result = getRecords()
#print(result["status"])
numOfRec = (result["hits"]["total"])
print("Records: ", numOfRec)

localRecordCounter = 1
remotePaginator = 1
resultSet = {}
while localRecordCounter < int(numOfRec):
    params["page"] = remotePaginator
    result = getRecords()
    for record in result["hits"]["hits"]:
        print(f"#{localRecordCounter}: {record['title']}")
        localRecordCounter += 1
        files = record.get("files", [])
        for f in files:
            print(f"{f['size']/1e6:.3f} MB") 

            size = f.get("size", 0)
            total_bytes += size
            
                

        page += 1
    remotePaginator += 1
    print(f"go to next records page {remotePaginator}")




print(f"Total size of {numOfRec} files in community '{COMMUNITY}': {total_bytes / 1e9:.3f} GB")
print(f"or  {total_bytes / 1e6:.3f} MB")
