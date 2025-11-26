import os
import requests
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Token aus der .env lesen
ACCESS_TOKEN = os.getenv("ZENODO_TOKEN")

ZENODO_API = "https://zenodo.org/api/records"
# Name der Community festlegen
COMMUNITY = "lory_hslu"  
page = 1
total_bytes = 0


headers = {}
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

params = {
        "communities": COMMUNITY,
        "size": 25,
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
