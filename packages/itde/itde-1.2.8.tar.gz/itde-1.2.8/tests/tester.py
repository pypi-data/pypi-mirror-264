# type: ignore
import os
import json
import sys
import shutil
import traceback
from enum import Enum
from httpx import ConnectError
from innertube import InnerTube
from innertube.errors import RequestError
from typing import Dict
from typing import Callable
from typing import List
from typing import Optional

TEST_PATH = os.path.dirname(__file__)
TEST_DATA = os.path.join(TEST_PATH, "test_data.json")
TEST_INNT = os.path.join(TEST_PATH, "innertube")
TEST_DUMP = os.path.join(TEST_PATH, "dumps")
ITDE_PATH = os.path.dirname(TEST_PATH)
sys.path.insert(0, ITDE_PATH)

from itde import extractor  # noqa
from itde import Container  # noqa
from itde import ITDEError  # noqa
from itde import CardShelf  # noqa


def clear(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


clear(TEST_INNT)
clear(TEST_DUMP)


class Tester:

    def __init__(self, save_data: bool = True) -> None:
        self.__innertube_client = InnerTube("WEB_REMIX")

        self.ext_log: List[str] = []  # extraction log
        self.ser_log: List[str] = []  # serialization log
        self.des_log: List[str] = []  # deserialization log
        self.dei_log: List[str] = []  # deserialization integrity log

        self.ext_containers: Dict[str, Optional[Container]] = {}
        self.des_containers: Dict[str, Optional[Container]] = {}

        self.save_data = save_data

        with open(TEST_DATA, mode="r") as file:
            test_data = json.loads(file.read())

        self.__test_sear = test_data["sear"]  # search tests
        self.__test_brow = test_data["brow"]  # browse tests
        self.__test_next = test_data["next"]  # next tests

    def test_search_extraction(self) -> None:
        for test in self.__test_sear:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.search(
                    query=test["query"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="sear",
                test_name=test["name"],
            )

    def test_browse_extraction(self) -> None:
        for test in self.__test_brow:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.browse(
                    browse_id=test["browse_id"],
                    params=test["params"],
                    continuation=test["continuation"],
                ),
                test_type="brow",
                test_name=test["name"],
            )

    def test_next_extraction(self) -> None:
        for test in self.__test_next:
            self.__do_extraction_test__(
                func=lambda: self.__innertube_client.next(
                    video_id=test["video_id"],
                    playlist_id=test["playlist_id"],
                    params=test["params"],
                    index=test["index"],
                    continuation=test["continuation"],
                ),
                test_type="next",
                test_name=test["name"],
            )

    def test_serialization(self) -> None:
        for name, container in self.ext_containers.items():
            try:
                dump = None if container is None else container.dump()
                if self.save_data:
                    with open(os.path.join(TEST_DUMP, f"{name}.json"), mode="w") as file:
                        json.dump(dump, file, indent=4)
                self.ser_log.append(f"{name} {Color.GREEN}[OK]{Color.RESET}")
            except Exception:
                traceback.print_exc()
                self.ser_log.append(f"{name} {Color.RED}[ERROR]{Color.RESET}")

    def test_deserialization(self) -> None:
        for filename in os.listdir(TEST_DUMP):
            with open(os.path.join(TEST_DUMP, filename), mode="r") as file:
                name = filename.split(".")[0]
                try:
                    data = json.loads(file.read())
                    container = Container()
                    container.load(data)
                    self.des_containers[name] = container
                    self.des_log.append(f"{name} {Color.GREEN}[OK]{Color.RESET}")
                except BaseException:
                    traceback.print_exc()
                    self.des_log.append(f"{name} {Color.RED}[ERROR]{Color.RESET}")

    def test_deserialization_integrity(self) -> None:
        for name, container in self.des_containers.items():
            if self.ext_containers[name] == container:
                self.dei_log.append(f"{name} {Color.GREEN}[OK]{Color.RESET}")
            else:
                self.dei_log.append(f"{name} {Color.RED}[ERROR]{Color.RESET}")
                print(f"{Color.BLUE} DESERIALIZED - {name}{Color.RESET}")
                print_container(container)
                print()
                print(f"{Color.BLUE} EXTRACTED - {name}{Color.RESET}")
                print_container(self.ext_containers[name])
                for i in range(len(self.ext_containers[name].contents)):
                    if self.ext_containers[name].contents[i] != container.contents[i]:
                        print(f"error {name}: {container.contents[i].name}")
 
    def __do_extraction_test__(self, func: Callable, test_type: str, test_name: str) -> None:
        name = f"{test_type}_{test_name}"
        log = f"{name} {Color.GREEN}[OK]{Color.RESET}"
        try:
            innertube_data = func()
            ext_container = extractor.extract(innertube_data)
            self.ext_containers[name] = ext_container
        except (ITDEError, RequestError, ConnectError) as error:
            print(f"{Color.BOLD}{Color.BLUE}+++ {name} +++{Color.RESET}")
            traceback.print_exc()
            self.ext_log.append(f"{name} {Color.RED}[ERROR]{Color.RESET}")
            if not isinstance(error, ITDEError):
                return
        else: 
            print(f"{Color.BLUE}{name}{Color.RESET}")
            if ext_container and ext_container.contents:
                print_container(ext_container)
            else:
                print("None")
            print()
        finally:
            self.ext_log.append(log)
            if self.save_data:
                with open(os.path.join(TEST_INNT, f"{name}.json"), mode="w") as file:
                    json.dump(innertube_data, file, indent=4)  # noqa


def print_container(container: Container) -> None:
    for shelf in container.contents:
        print(f"{Color.LIGHT_GREEN}{shelf.name}{Color.RESET}")
        for item in shelf:
            print(f"{str(item)[:]}")


class Color(Enum):
    GREEN = "\033[92m"
    LIGHT_GREEN = "\033[1;92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    BOLD = "\033[;1m"
    CYAN = "\033[1;36m"
    LIGHT_CYAN = "\033[1;96m"
    LIGHT_GREY = "\033[1;37m"
    DARK_GREY = "\033[1;90m"
    BLACK = "\033[1;30m"
    WHITE = "\033[1;97m"
    INVERT = "\033[;7m"
    RESET = "\033[0m"

    def __str__(self) -> str:
        return self.value


def main():
    tester = Tester()
    tester.test_search_extraction()
    tester.test_browse_extraction()
    tester.test_next_extraction()

    tester.test_serialization()
    tester.test_deserialization()
    tester.test_deserialization_integrity()

    print("-- Extractions --")
    for log in tester.ext_log:
        print(log)

    print("-- Serialization --")
    for log in tester.ser_log:
        print(log)

    print("-- Deserialization --")
    for log in tester.des_log:
        print(log)

    print("-- Deserialization Integrity --")
    for log in tester.dei_log:
        print(log)

if __name__ == "__main__":
    main()
