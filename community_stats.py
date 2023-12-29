import requests
import argparse
import pandas as pd

# Erstelle den ArgumentParser
parser = argparse.ArgumentParser(description='Fetch all records of a Zenodo Community via REST-API', usage="python3 community_stats.py --community={YOUR_COMMUNITY}")
# Füge das Argument 'shoulder' hinzu
parser.add_argument('--community', '-c', required=True, help='Your Zenodo-Community', )
parser.add_argument('--size', '-s', required=False, help='Define your costum number of records per one API-Call', )
parser.add_argument('--output', '-o', required=True, help='Name of Output-XLS-File like Output_2023.xlsx', )
# Parse die Argumente
args = parser.parse_args()

zenodoRestUrl = "https://zenodo.org/api/records"
headers = {}
headers["Content-Type"] = "application/json"

# Zugriff auf das Argument 'Size'    
if args.size:
    size = args.size
else:
    size = "100" 

params = { "communities":  args.community, "size": size}


def getRecords():
    r = requests.get(f"{zenodoRestUrl}", params=params, headers=headers)
    return r.json()

result = getRecords()
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