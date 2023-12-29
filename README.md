# Zenodo Statistics

This python script allows you to calculate statistics of your [Zenodo](https://zenodo.org) records and write them into an XLS-File.

* Records are parsed using the [Zenodo REST-API](https://developers.zenodo.org/#records)
* Zenodo store several download and view numbers for each record, which looks like
```json
 "stats": {
          "downloads": 10,
          "unique_downloads": 2,
          "unique_views": 2,
          "version_downloads": 10,
          "version_unique_downloads": 2,
          "version_unique_views": 2,
          "version_views": 6,
          "views": 6
        },
```
* Write an output as *xlsx.

## Dependencies

This script makes usage of the following python libraries

* `Requests`
* `argparse`
* `pandas`

## Run `community_stats.py` - Calculate by Communities

* Search for records by a given Zenodo-Community name
* The Script sums up `version_unique_downloads` and `version_unique_views` for each community detected in a record

```bash
python3 community_stats.py -c {YOUR_COMMUNITY} -o {YOUR_OUTPUTFILE.xlsx}
```
