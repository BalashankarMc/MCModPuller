from requests import get, HTTPError
from json import loads
from collections import deque
from os import path
from typing import Dict, List

MODRINTH = "https://api.modrinth.com/v2"

# Dictionaries containing every version of Minecraft supported by Fabric, Forge, NeoForge, and Quilt

fabricVersions: Dict[str, List[str]] = {
    "1.14": ["1.14", "1.14.1", "1.14.2", "1.14.3", "1.14.4"],
    "1.15": ["1.15", "1.15.1", "1.15.2"],
    "1.16": ["1.16", "1.16.1", "1.16.2", "1.16.3", "1.16.4", "1.16.5"],
    "1.17": ["1.17", "1.17.1"],
    "1.18": ["1.18", "1.18.1", "1.18.2"],
    "1.19": ["1.19", "1.19.1", "1.19.2", "1.19.3", "1.19.4"],
    "1.20": ["1.20", "1.20.1", "1.20.2", "1.20.3", "1.20.4", "1.20.5", "1.20.6"],
    "1.21": ["1.21", "1.21.1", "1.21.2", "1.21.3", "1.21.4", "1.21.5", "1.21.6", "1.21.7", "1.21.8", "1.21.9", "1.21.10"]
}
forgeVersions:  Dict[str, List[str]] = {
    "1.1":  ["1.1"], "1.2":  ["1.2.3", "1.2.4", "1.2.5"], "1.3":  ["1.3.2"],
    "1.4":  ['1.4', '1.4.1', '1.4.2', '1.4.3', '1.4.4', '1.4.5', '1.4.6', '1.4.7'],
    "1.5":  ['1.5', '1.5.1', '1.5.2'], "1.6":  ['1.6.1', '1.6.2', '1.6.3', '1.6.4'],
    "1.7":  ["1.7.2", "1.7.10"], "1.8":  ["1.8", "1.8.8", "1.8.9"],
    "1.9":  ["1.9", "1.9.4"], "1.10": ["1.10", "1.10.2"],
    "1.11": ["1.11.1", "1.11.2"], "1.12": ['1.12', '1.12.1', '1.12.2'],
    "1.13": ["1.13.2"], "1.14": ['1.14.2', '1.14.3', '1.14.4'],
    "1.15": ['1.15', '1.15.1', '1.15.2'], "1.16": ['1.16.1', '1.16.2', '1.16.3', '1.16.4', '1.16.5'],
    "1.17": ["1.17.1"], "1.18": ['1.18', '1.18.1', '1.18.2'],
    "1.19": ['1.19', '1.19.1', '1.19.2', '1.19.3', '1.19.4'],
    "1.20": ['1.20', '1.20.1', '1.20.2', '1.20.3', '1.20.4', '1.20.5', '1.20.6'],
    "1.21": ['1.21', '1.21.1', '1.21.2', '1.21.3', '1.21.4', '1.21.5', '1.21.6', '1.21.7', '1.21.8', '1.21.9']
}
neoVersions:    Dict[str, List[str]] = {
    "1.20": ['1.20.1', '1.20.2', '1.20.3', '1.20.4', '1.20.5', '1.20.6'],
    "1.21": ['1.21', '1.21.1', '1.21.2', '1.21.3', '1.21.4', '1.21.5', '1.21.6', '1.21.7', '1.21.8', '1.21.9', '1.21.10']
}
quiltVersions:  Dict[str, List[str]] = {
    "1.14": ['1.14.4'], "1.15": ['1.15', '1.15.1', '1.15.2'],
    "1.16": ['1.16.1', '1.16.2', '1.16.3', '1.16.4', '1.16.5'],
    "1.17": ['1.17', '1.17.1'], "1.18": ['1.18', '1.18.1', '1.18.2'],
    "1.19": ['1.19', '1.19.1', '1.19.2', '1.19.3', '1.19.4'],
    "1.20": ['1.20', '1.20.1', '1.20.2', '1.20.3', '1.20.4', '1.20.5', '1.20.6'],
    "1.21": ['1.21', '1.21.1', '1.21.2', '1.21.3', '1.21.4', '1.21.5', '1.21.6', '1.21.7', '1.21.8', '1.21.9', '1.21.10']
}

def constructURL(mod: str, ver: str, loader: str) -> str:
    """
    Simple function to construct the Modrinth URL using the mod name, version, and the loader.
    """
    return f"{MODRINTH}/project/{mod}/version?game_versions=[\"{ver}\"]&loaders=[\"{loader}\"]"

def getDownloadURLs(mod: str, ver: str, loader: str) -> set | int:
    """
    Function to obtain a set consisting of the download links of the specified mod and it's dependencies.
    Returns the set of download links on success and returns the HTTP Error code on failiure
    """
    try:
        mods = deque([mod])
        urls = set()
        processedMods = set()
        while mods:
            current = mods.popleft()
            if current in processedMods:
                continue
            processedMods.add(current)
            print(current)
            url = constructURL(current, ver, loader)
            request = get(url)
            request.raise_for_status()
            modInfo = loads(request.content.decode())
            dependencies = modInfo[0]["dependencies"]
            downloadLink = modInfo[0]["files"][0]["url"]
            urls.add(downloadLink)
            for dep in dependencies:
                mods.append(dep["project_id"])
        return urls
    

    except HTTPError:
        print(f"An HTTP Error occured while searching for the mod! Error Code: {request.status_code}")
        print(f"The URL was {url}")
        return request.status_code

def pullMods(urls: list[str], dest: str) -> int:
    """
    Function to download the mods to the given destination and return:
    0: On a successful download
    -1: On an IO Error
    An HTTP Error code: On an HTTP Error
    """
    try:
        for url in urls:
            file = get(url)
            file.raise_for_status()
            filename = url.split('/')[-1].split('-')[0].capitalize() + ".jar"
            with open(path.join(dest, filename), 'w') as modFile:
                modFile.write(file.content)
        return 0
    except HTTPError:
        print(f"An HTTP Error occured while downloading the mod {filename.removesuffix(".jar")}! Error Code: {file.status_code}")
        print(f"The URL was {url}")
        return file.status_code
    except IOError:
        print(f"An IO Error occured while downloading the mod {filename.removesuffix(".jar")}!")
        return -1