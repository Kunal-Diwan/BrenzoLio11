import urllib.request as url

VERSION = "1.0.2"
APIURL = "http://api.github.com/repos/"


def vercheck() -> str:
    return str(VERSION)


def getData(repoURL):
    try:
        with url.urlopen(APIURL + repoURL + "/releases") as data_raw:
            return json.loads(data_raw.read().decode())
    except Exception:
        return None


def getReleaseData(repoData, index):
    if index < len(repoData):
        return repoData[index]
    else:
        return None


def getAuthor(releaseData):
    if releaseData is None:
        return None
    return releaseData['author']['login']


def getAuthorUrl(releaseData):
    if releaseData is None:
        return None
    return releaseData['author']['html_url']


def getReleaseName(releaseData):
    if releaseData is None:
        return None
    return releaseData['name']


def getReleaseDate(releaseData):
    if releaseData is None:
        return None
    return releaseData['published_at']


def getAssetsSize(releaseData):
    if releaseData is None:
        return None
    return len(releaseData['assets'])


def getAssets(releaseData):
    if releaseData is None:
        return None
    return releaseData['assets']


def getBody(releaseData):
    if releaseData is None:
        return None
    return releaseData['body']


def getReleaseFileName(asset):
    return asset['name']


def getReleaseFileURL(asset):
    return asset['browser_download_url']


def getDownloadCount(asset):
    return asset['download_count']


def getSize(asset):
    return asset['size']
