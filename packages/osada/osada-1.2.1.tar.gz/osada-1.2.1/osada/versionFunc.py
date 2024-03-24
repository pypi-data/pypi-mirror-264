versions = {
    "1.0.0": "12/30/2021",
    "1.0.1": "01/03/2022",
    "1.1.0" : "01/05/2022",
    "1.2.0" : "03/23/2024",
    "1.2.1" : "03/23/2024",
    }


__version__ = list(versions.keys())[-1]
version_info = f"{__version__} ({versions[__version__]})"


def getVersion():
    lst = list(map(int, __version__.split(".")))
    return len(lst), lst

