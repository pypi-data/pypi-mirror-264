import requests

class DownloadableLink:
    def __init__(self, link, fileType) -> None:
        self.link = link
        self.fileType = fileType

class DataDownloader:
    def __init__(self, downloadableLinks: list[DownloadableLink]) -> None:
        super().__init__()
        self.downloadableLinks = downloadableLinks

    def directDataDownload(self):
        for i in range(len(self.downloadableLinks)):
            linkItem = self.downloadableLinks[i]
            response = requests.get(linkItem.link)
            with open(f"./temp/{i}.{linkItem.fileType}", "wb") as f:
                f.write(response.content)

    @staticmethod
    def singleDirectDownload(
        link,
        filetype,
        insertString="",
        appendString="",
        proxies=None,
        saveLocation=None,
    ) -> str:
        response = requests.get(link, proxies=proxies)
        outfile = (
            saveLocation
            if saveLocation != None
            else f"./temp/{getRandomString(10)}.{filetype}"
        )
        with open(outfile, "wb") as f:
            f.write(
                bytes(insertString, encoding="utf-8")
                + response.content
                + bytes(appendString, encoding="utf-8")
            )
        return outfile


import random, string


def getRandomString(N):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=N))