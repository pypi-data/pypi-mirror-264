from typing import Optional, Dict
from .types import EndpointType


class Endpoint:
    def __init__(
        self,
        params: Optional[str] = None,
        continuation: Optional[str] = None,
    ) -> None:
        self.params = params
        self.continuation = continuation

    def __repr__(self) -> str:
        return (
            "Endpoint{"
            f"params={self.params}, "
            f"continuation={self.continuation}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.params, self.continuation))

    def dump(self) -> Dict:
        return {
            "params": self.params,
            "continuation": self.continuation
        }

    def load(self, data: Dict) -> None:
        self.params = data["params"]
        self.continuation = data["continuation"]


class BrowseEndpoint(Endpoint):
    def __init__(self, browse_id: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.browse_id = browse_id

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", browse_id={self.browse_id}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BrowseEndpoint):
            return (
                self.params == __value.params and
                self.browse_id == __value.browse_id and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.params, self.continuation, self.browse_id))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.BROWSE.value,
            "browse_id": self.browse_id
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.browse_id = data["browse_id"]


class SearchEndpoint(Endpoint):
    def __init__(self, query: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query = query

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", query={self.query}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SearchEndpoint):
            return (
                self.query == __value.query and
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.params, self.continuation, self.query))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.SEARCH.value,
            "query": self.query
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.query = data["query"]


class WatchEndpoint(Endpoint):
    def __init__(
        self,
        video_id: Optional[str] = None,
        playlist_id: Optional[str] = None,
        index: Optional[int] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.video_id = video_id
        self.index = index
        self.playlist_id = playlist_id

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] + 
            f", video_id={self.video_id}"
            f", playlist_id={self.playlist_id}"
            f", index={self.index}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, WatchEndpoint):
            return (
                self.index == __value.index and
                self.params == __value.params and
                self.video_id == __value.video_id and
                self.playlist_id == __value.playlist_id and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.params, 
            self.continuation, 
            self.video_id, 
            self.playlist_id, 
            self.index
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.WATCH.value,
            "video_id": self.video_id,
            "playlist_id": self.playlist_id,
            "index": self.index
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.video_id = data["video_id"]
        self.playlist_id = data["playlist_id"]
        self.index = data["index"]


class UrlEndpoint(Endpoint):
    def __init__(self, url: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url = url

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", url={self.url}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, UrlEndpoint):
            return (
                self.url == __value.url and
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.params, self.continuation, self.url))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": EndpointType.URL.value,
            "url": self.url
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.url = data["url"]
