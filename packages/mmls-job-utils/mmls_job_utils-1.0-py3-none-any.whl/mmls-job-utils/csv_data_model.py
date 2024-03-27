import pandas
from data_download import DataDownloader


class CsvDataModel:
    def __init__(
        self,
        requiredColumns,
        weburl=None,
        datasetID=None,
        accountIDField=None,
        lcfilename=None,
        pkfield=None,
        isXlsx=False,
        forceRandomSave=False,
    ) -> None:
        if (not weburl) and (not lcfilename) and (not datasetID):
            raise Exception("Either weburl or lcfilename or datasetID must be provided")
        if (
            (weburl and lcfilename)
            or (weburl and datasetID)
            or (lcfilename and datasetID)
        ):
            raise Exception(
                "Only one of weburl or lcfilename or datasetID must be provided on creation"
            )
        self.datasetID = datasetID
        # lc_filename stands for local_filename
        self.weburl = weburl
        self.lcfilename = lcfilename
        self.requiredColumns = requiredColumns
        self.pkfield = pkfield
        self.accountIDField = accountIDField
        self.csvData: pandas.DataFrame | None = None
        self.isXlsx = isXlsx
        self.forceRandomSave = forceRandomSave

    def downloadWebData(self, addHead: list[str] = []):
        if not self.weburl:
            return self
            # raise Exception("weburl is not provided")
        self.lcfilename = DataDownloader.singleDirectDownload(
            self.weburl,
            "csv",
            insertString=",".join([f'"{item}"' for item in addHead]) + "\n",
            saveLocation=self.lcfilename
            if self.lcfilename and not (self.forceRandomSave)
            else None,
        )
        return self

    def combineWith(
        self, others: list["CsvDataModel"], filterMobileHomes=True, encoding=None
    ):
        outdf = (
            pandas.read_csv(
                self.lcfilename, usecols=self.requiredColumns, encoding=encoding
            )
            if not (self.isXlsx)
            else pandas.read_excel(
                self.lcfilename, usecols=self.requiredColumns, engine="openpyxl"
            )
        )

        if filterMobileHomes and self.accountIDField:
            outdf = outdf[outdf[self.accountIDField].str.startswith("M")]

        for other in others:
            otherdf = (
                pandas.read_csv(
                    other.lcfilename, usecols=other.requiredColumns, encoding=encoding
                )
                if not (other.isXlsx)
                else pandas.read_excel(
                    other.lcfilename, usecols=other.requiredColumns, engine="openpyxl"
                )
            )
            outdf = outdf.merge(
                otherdf,
                how="left",
                left_on=self.pkfield,
                right_on=other.pkfield,
            )

        return outdf

    # takes the lcfilename field and uses it to read the csv file and save the df to self.csvData
    def loadcsv(self, **kwargs) -> "CsvDataModel":
        if self.lcfilename is None:
            raise Exception("lcfilename is not provided")

        self.csvData = pandas.read_csv(
            self.lcfilename, usecols=self.requiredColumns, **kwargs
        )
        return self

    def filterMobileHomes(self) -> "CsvDataModel":
        if self.csvData is None:
            raise Exception("csvData is not provided, run loadcsv() first")

        if self.accountIDField:
            self.csvData = self.csvData[
                self.csvData[self.accountIDField].str.startswith("M")
            ]

        return self

    def export(self, filename):
        self.csvData.to_csv(filename, index=False)

        return filename