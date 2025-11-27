import helper as ModHelper
from os.path import join, expanduser, isdir
from os import listdir
from simple_term_menu import TerminalMenu
from colorama import Fore, init
from typing import Dict, Tuple, List, Set

def getLoaderVer(loaders: List[str]) -> Tuple[int, Dict]:
    menu = TerminalMenu(loaders, title="Select the Mod Loader:").show()
    match menu:
        case 0:
            versions = ModHelper.fabricVersions
        case 1:
            versions = ModHelper.forgeVersions
        case 2:
            versions = ModHelper.neoVersions
        case 3:
            versions = ModHelper.quiltVersions
        case _:
            print("If you are seeing this, it means something went wrong while finding your loader, or it's not supported yet.")
    return menu, versions
            
def getPath(check, title: str, choose: str) -> str:
    currentPath = expanduser('~')
    while True:
        dirs = [file for file in listdir(currentPath) if check(join(currentPath, file))]
        options = dirs + [choose]
        newPath = options[TerminalMenu(options, title=title).show()]
        if newPath == options[-1]:
            break
        currentPath = join(currentPath, newPath)
    return currentPath

def getVersion(versions: Dict) -> str:
    versionMajor = list(versions.keys())[TerminalMenu(versions.keys(), title="Select the Major Version").show()]
    return versions[versionMajor][TerminalMenu(versions[versionMajor], title="Select the Full Version").show()]

def main() -> None:
    print(Fore.CYAN + "---------- Minecraft Mod Manager ----------")
    print(Fore.RED  + "     ----- Made by BalashankarMc -----     ")

    loaders = ["Fabric", "Forge", "NeoForge", "Quilt"]
    loader, versions = getLoaderVer(loaders)    
    version: str = getVersion(versions)
    path: str = getPath(isdir, "Choose the directory to download mods to", "Choose this directory")

    menu = TerminalMenu(["I will enter them manually", "From a file"], title="Source to fetch Mod Names from:").show()
    if menu == 0:
        while True:
            mod = input("Enter the mod name:")
            urls: Set = ModHelper.getDownloadURLs(mod, version, loaders[loader].lower())
            return ModHelper.pullMods(urls, path)
    elif menu == 1:
        urls = set()
        file = getPath(lambda path: True, "Choose the file to pull Mod Names from", "Choose this file")
        with open(file, 'r') as modFile:
            for mod in modFile:
                urls |= ModHelper.getDownloadURLs(mod, version, loaders[loader].lower())
        return ModHelper.pullMods(urls, path)

if __name__ == "__main__":
    init(True)
    main()