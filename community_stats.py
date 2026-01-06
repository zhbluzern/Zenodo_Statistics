import requests
import argparse
import pandas as pd
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()

# Token aus der .env lesen
ACCESS_TOKEN = os.getenv("ZENODO_TOKEN")

# Erstelle den ArgumentParser
parser = argparse.ArgumentParser(description='Fetch all records of a Zenodo Community via REST-API', usage="python3 community_stats.py --community {YOUR_COMMUNITY} --output {YOUR_OUTPUTFile.xlsx}")
# Füge das Argument 'shoulder' hinzu
parser.add_argument('--community', '-c', required=True, help='Your Zenodo-Community', )
parser.add_argument('--size', '-s', required=False, help='Define your costum number of records per one API-Call', )
parser.add_argument('--output', '-o', required=True, help='Name of Output-XLS-File like Output_2023.xlsx', )
# Parse die Argumente
args = parser.parse_args()

zenodoRestUrl = "https://zenodo.org/api/records"
headers = {}
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"

# Zugriff auf das Argument 'Size'    
if args.size:
    size = args.size
else:
    size = "100" 

params = { "communities":  args.community, "size": size}


def getRecords():
    r = requests.get(f"{zenodoRestUrl}", params=params, headers=headers, timeout=30)
    r.raise_for_status()
    
    ctype = r.headers.get("Content-Type", "")
    if "application/json" in ctype:
        try:
            return r.json()
        except ValueError as e:  # JSONDecodeError ist Unterklasse von ValueError
            # Debug-Ausgabe: zeige Beginn des Antworttexts
            print("JSON parsing failed. First 500 chars of response:\n", r.text[:500])
            raise
    else:
        # Nicht-JSON – z. B. HTML-Fehlerseite oder leerer Text
        print("Unexpected Content-Type:", ctype)
        print("Status:", r.status_code)
        print("First 500 chars of response:\n", r.text[:500])
        raise RuntimeError("API did not return JSON")

    #return r.json()

result = getRecords()
#print(result)
print(f"Fetched {len(result['hits']['hits'])} records from Zenodo Community: {args.community}")
numOfRec = (result["hits"]["total"])

localRecordCounter = 1
remotePaginator = 1
resultSet = {}
while localRecordCounter < int(numOfRec):
    params["page"] = remotePaginator
    result = getRecords()
    for record in result["hits"]["hits"]:
        print(f"#{localRecordCounter}: {record['doi']}")
        for communities in record["metadata"]["communities"]:
            print(communities["id"])
            try:
                resultSet[communities["id"]]["version_unique_downloads"] += record["stats"]["version_unique_downloads"]
                resultSet[communities["id"]]["version_unique_views"] += record["stats"]["version_unique_views"]
                resultSet[communities["id"]]["numOfRecords"] += 1
            except KeyError:
                resultSet.update({communities["id"] : {"version_unique_downloads" : record["stats"]["version_unique_downloads"], 
                                                       "version_unique_views" : record["stats"]["version_unique_views"],
                                                       "numOfRecords" : 1   }})

        localRecordCounter += 1
    
    remotePaginator += 1
    print(f"go to next {size} reoords page {remotePaginator}")

    #break

print(f"Number of Records in Community {args.community}: {result['hits']['total']}")

#Schreibe Metadaten (resultSet) in ein XLS-File zur Weiterbearbeitung
df = pd.DataFrame(resultSet) 
df = df.transpose()
print(df.head())
df.to_excel(args.output) 