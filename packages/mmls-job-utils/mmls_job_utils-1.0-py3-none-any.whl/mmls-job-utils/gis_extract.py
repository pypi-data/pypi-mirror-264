import requests
from data_download import DataDownloader
from csv_data_model import CsvDataModel


class GisExtract:
    def __init__(self, dataInfoList: list[CsvDataModel]) -> None:
        self.dataInfoList = dataInfoList

    def extract(self):
        for ds in self.dataInfoList:
            latestDataDetails = requests.get(
                f"https://opendata.arcgis.com/api/v3/datasets/{ds.datasetID}/downloads?where=1%3D1",
                json={
                    "format": "csv",
                    "where": "1=1",
                },
            )

            if not (latestDataDetails.ok):
                continue

            latestDataDetails = latestDataDetails.json()
            spatialRef = list(
                filter(
                    lambda x: x["attributes"]["format"] == "csv",
                    latestDataDetails["data"],
                )
            )[0]["attributes"]["source"]["spatialRefId"]

            outfilename = DataDownloader.singleDirectDownload(
                f"https://opendata.arcgis.com/api/v3/datasets/{ds.datasetID}/downloads/data?format=csv&spatialRefId={spatialRef}&where=1%3D1",
                "csv",
            )

            ds.lcfilename = outfilename
            yield ds