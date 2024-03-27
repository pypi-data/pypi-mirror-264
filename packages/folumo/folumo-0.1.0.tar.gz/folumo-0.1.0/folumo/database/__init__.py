from json import dumps as dumpJSON
from json import loads as loadJSON

from pickle import dumps as dumpPICKLE
from pickle import loads as loadPICKLE

from os import remove

from typing import Union


# ////////////////////////////
# //START/////ERRORS//////////
# ////////////////////////////


class dbError(Exception):
    pass


class dbInvalidArchitectureError(dbError):
    pass


class dbInvalidKeyOrValueError(dbError):
    pass

# ////////////////////////////
# ////END/////ERRORS//////////
# ////////////////////////////


letters = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
numbers = "1234567890"
symbols = "!@#$%^&*()_+-=*/.,<>{}[]\\|?"

class database:
    def __init__(self, path: str, architecture: str = "Line-Text", compressIfByte: bool = False):
        """
        This database auto saves on change.

        Architecture:
            "Line-Text"
            "JSON"
            "Line-Byte"
            "PICKLE"

        :param path:
        :param architecture:
        """

        if architecture not in ["Line-Text", "JSON", "Line-Byte", "PICKLE"]:
            raise dbInvalidArchitectureError("Invalid architecture")

        self.path = path
        self.arch = architecture
        self.data: list[str] | dict = ["""var:'a123'"""]

    def get(self, key: any, default: any = None) -> Union[any, Exception]:
        """
        Using get retries any data in database based on key.

        :param default:
        :param key:
        :return any:
        """

        if self.arch == "Line-Text":
            if ":" in key:
                raise dbInvalidKeyOrValueError
            for line in self.data:
                print(f"{line = }")
                if line.find(key) == 0:
                    dataNew = line.split(":", 1)

                    return eval(dataNew[1])
            return default

        elif self.arch == "JSON":
            return self.data.get(key, default)

        elif self.arch == "Line-Byte":
            if ":" in key:
                raise dbInvalidKeyOrValueError
            for line in self.data:
                lineNew: str = line.decode()

                print(f"{lineNew = }")
                if lineNew.find(key) == 0:
                    dataNew = lineNew.split(":", 1)

                    return eval(dataNew[1])
            return default

        elif self.arch == "PICKLE":
            return self.data.get(key, default)

    def set(self, key: any, value: any) -> bool | tuple[bool, Exception]:
        """
        Using set sets data at provided key.

        (auto saves on execute)

        :param key:
        :param value:
        :return:
        """

        if self.arch == "Line-Text":
            if ":" in key:
                raise dbInvalidKeyOrValueError
            for line in self.data:
                print(f"{line = }")
                if line.find(key) == 0:
                    dataNew = line.split(":", 1)

                    return eval(dataNew[1])
            return default

        elif self.arch == "JSON":
            return self.data.get(key, default)

        elif self.arch == "Line-Byte":
            if ":" in key:
                raise dbInvalidKeyOrValueError
            for line in self.data:
                lineNew: str = line.decode()

                print(f"{lineNew = }")
                if lineNew.find(key) == 0:
                    dataNew = lineNew.split(":", 1)

                    return eval(dataNew[1])
            return default

        elif self.arch == "PICKLE":
            return self.data.get(key, default)

    def delete(self, key: any) -> bool | tuple[bool, Exception]:
        """
        Using delete will delete data at provided key.

        (auto saves on execute)

        :param key:
        :return:
        """

    def __save(self) -> bool | tuple[bool, Exception]:
        """
        Only use if you need to manually save database.
        :return:
        """

    def dbDel(self) -> bool | tuple[bool, Exception]:
        """
        !!!DELETES!!! database and all its data.
        :return:
        """
        try:
            remove(self.path)
            return True
        except Exception as e:
            return False, e


def test():
    a = database("")
    print(type(a.get("var")))


if __name__ == "__main__":
    test()
