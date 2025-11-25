import helper as ModHelper
from os.path import join, expanduser, isdir
from os import listdir
from simple_term_menu import TerminalMenu
from colorama import Fore, init

def main() -> None:
    print(Fore.CYAN + "---------- Minecraft Mod Manager ----------")
    print(Fore.RED  + "       --- Made by BalashankarMc ---       ")
    loaders = ["Fabric", "Forge", "NeoForge", "Quilt"]
    try:
        while True:
            loader = loaders[TerminalMenu(loaders, title="Select the Mod Loader:").show()].lower()
            match loader:
                case "fabric":
                    versions = ModHelper.fabricVersions
                    break
                case "forge":
                    versions = ModHelper.forgeVersions
                    break
                case "neoforge":
                    versions = ModHelper.neoVersions
                    break
                case "quilt":
                    versions = ModHelper.quiltVersions
                    break
                case _:
                    print("If you are seeing this, it means something went wrong while finding your loader, or it's not supported yet.")
                    break
    except ValueError:
        print("Choose a valid Mod Loader!")
    
    versionMajor = list(versions.keys())[TerminalMenu(versions.keys(), title="Select the Major Version").show()]
    version = versions[versionMajor][TerminalMenu(versions[versionMajor], title="Select the Full Version").show()]
    currentPath = expanduser('~')
    while True:
        dirs = [file for file in listdir(currentPath) if isdir(join(currentPath, file))]
        options = dirs + ["Choose this directory"]
        newPath = options[TerminalMenu(options, title="Choose the directory to download mods to").show()]
        if newPath == options[-1]:
            break
        currentPath = join(currentPath, newPath)
    

if __name__ == "__main__":
    init(True)
    main()