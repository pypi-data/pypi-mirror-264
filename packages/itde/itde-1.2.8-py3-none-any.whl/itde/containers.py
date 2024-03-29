from typing import List, Optional, Dict
from .items import Item
from .endpoints import Endpoint
from .types import ShelfType
from .utils import get_endpoint, get_items, get_item


class Shelf(List[Item]):
    def __init__(
        self,
        name: Optional[str] = None,
        endpoint: Optional[Endpoint] = None,
        continuation: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.name = name
        self.endpoint = endpoint
        self.continuation = continuation

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Shelf):
            return (
                self.name == __value.name
                and self.endpoint == __value.endpoint
                and self.continuation == __value.continuation
                and super().__eq__(__value)
            )
        else:
            return False

    def __repr__(self) -> str:
        return (
            "Shelf{"
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"continuation={self.continuation}, "
            f"items={super().__repr__()}"
            "}"
        )

    def dump(self) -> Dict:
        return {
            "type": ShelfType.SHELF.value,
            "name": self.name,
            "endpoint": None if self.endpoint is None else self.endpoint.dump(),
            "continuation": self.continuation,
            "items": [item.dump() for item in self]
        }

    def load(self, data: Dict) -> None:
        self.name = data["name"]
        self.endpoint = None if data["endpoint"] is None else get_endpoint(data["endpoint"])
        self.continuation = data["continuation"]
        for item in get_items(data["items"]):
            self.append(item)


class CardShelf(Shelf):
    def __init__(self, item: Optional[Item] = None) -> None:
        super().__init__()
        self.item = item

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CardShelf):
            return (
                self.name == __value.name
                and self.endpoint == __value.endpoint
                and self.continuation == __value.continuation
                and self.item == __value.item
                and super().__eq__(__value)
            )
        else:
            return False

    def __str__(self) -> str:
        return "CardShelf{" f"{self.item}, " + super().__str__()[6:]

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ShelfType.CARD_SHELF.value,
            "item": None if self.item is None else self.item.dump(),
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.item = get_item(data["item"])


class Container:
    def __init__(
        self,
        header: Optional[Item] = None,
        contents: Optional[List[Shelf]] = None
    ) -> None:
        self.header = header
        if contents is None:
            contents = []
        self.contents = contents

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Container):
            return self.header == __value.header and self.contents == __value.contents
        else:
            return False

    def __str__(self) -> str:
        return (
            "Container{"
            f"header={self.header}, "
            f"contents={self.contents}"
            "}"
        )

    def dump(self) -> Dict:
        return {
            "header": None if self.header is None else self.header.dump(),
            "contents": None if self.contents is None else [shelf.dump() for shelf in self.contents]
        }

    def load(self, data: Dict) -> None:
        self.header = None if data["header"] is None else get_item(data["header"])
        for shelf_data in data["contents"]:
            if shelf_data["type"] == ShelfType.SHELF.value:
                shelf = Shelf()
            elif shelf_data["type"] == ShelfType.CARD_SHELF.value:
                shelf = CardShelf()
            else:
                raise ValueError("Invalid type")
            shelf.load(shelf_data)
            self.contents.append(shelf)
