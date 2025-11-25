from requests import get, HTTPError
from json import loads
from subprocess import run
from collections import deque
from os import path
from typing import Dict, List

MODRINTH = "https://api.modrinth.com/v2"


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
forgeVersions: Dict[str, List[str]] = {
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
neoVersions: Dict[str, List[str]] = {
    "1.20": ['1.20.1', '1.20.2', '1.20.3', '1.20.4', '1.20.5', '1.20.6'],
    "1.21": ['1.21', '1.21.1', '1.21.2', '1.21.3', '1.21.4', '1.21.5', '1.21.6', '1.21.7', '1.21.8', '1.21.9', '1.21.10']
}
quiltVersions: Dict[str, List[str]] = {
    "1.14": ['1.14.4'], "1.15": ['1.15', '1.15.1', '1.15.2'],
    "1.16": ['1.16.1', '1.16.2', '1.16.3', '1.16.4', '1.16.5'],
    "1.17": ['1.17', '1.17.1'], "1.18": ['1.18', '1.18.1', '1.18.2'],
    "1.19": ['1.19', '1.19.1', '1.19.2', '1.19.3', '1.19.4'],
    "1.20": ['1.20', '1.20.1', '1.20.2', '1.20.3', '1.20.4', '1.20.5', '1.20.6'],
    "1.21": ['1.21', '1.21.1', '1.21.2', '1.21.3', '1.21.4', '1.21.5', '1.21.6', '1.21.7', '1.21.8', '1.21.9', '1.21.10']
}

def findUser() -> str:
    user = run(["whoami"], capture_output=True, text=True)
    if user.returncode == 0:
        return user.stdout.strip()
    
    currentDir = path.abspath("./")
    if currentDir.startswith("/home/"):
        currentDir = currentDir.removeprefix("/home/")
        user = currentDir.split('/')[0]
        return user
    
    if currentDir.startswith("C:\\Users\\"):
        currentDir = currentDir.removeprefix("C:\\Users\\")
        user = currentDir.split("\\")[0]
        return user

    return input("Could not find your username, enter it manually: ").lower().strip()

def constructURL(mod: str, ver: str, loader: str):
    return f"{MODRINTH}/project/{mod}/version?game_versions=[\"{ver}\"]&loaders=[\"{loader}\"]"

def getDownloads(mod: str, ver: str, loader: str):
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
        print(f"An HTTPS Error occured! Error Code: {request.status_code}")
        print(f"The URL was {url}")

getDownloads(input("Enter a mod name:"), "1.21.10",  "fabric")