# type: ignore
import itde.utils as utils
from datetime import date, time
from typing import List, Optional, Dict
from .types import ItemType
from .endpoints import Endpoint


class Item:
    def __init__(
        self,
        name: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        endpoint: Optional[Endpoint] = None,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.thumbnail_url = thumbnail_url
        self.endpoint = endpoint
        self.description = description

    def __repr__(self) -> str:
        return (
            "Item{"
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"thumbnail_url={self.thumbnail_url}, "
            f"description={self.description}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
        ))

    def dump(self) -> Dict:
        return {
            "type": None,
            "name": self.name,
            "endpoint": None if self.endpoint is None else self.endpoint.dump(),
            "thumbnail_url": self.thumbnail_url,
            "description": self.description
        }

    def load(self, data: Dict) -> None:
        self.name = data["name"]
        self.thumbnail_url = data["thumbnail_url"]
        self.description = data["description"]
        self.endpoint = None if data["endpoint"] is None else utils.get_endpoint(data["endpoint"])


class ArtistItem(Item):
    def __init__(self, subscribers: Optional[int] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers = subscribers

    def __str__(self) -> str:
        return super().__str__()[:-1] + f", subscribers={self.subscribers}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ArtistItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.subscribers == __value.subscribers
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
            self.subscribers,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.ARTIST.value,
            "subscribers": self.subscribers
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.subscribers = data["subscribers"]


class VideoItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        views: Optional[int] = None,
        artist_items: Optional[List] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.views = views
        self.artist_items = artist_items

    def __str__(self) -> str:
        return (
            super().__str__()[:-1] + 
            f", length={self.length}"
            f", views={self.views}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, VideoItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.length == __value.length
                and self.views == __value.views
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
            self.length,
            self.views,
            self.artist_items,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.VIDEO.value,
            "views": self.views,
            "artist_items": [a.dump() for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]
        self.artist_items = utils.get_artist_items(data["artist_items"])
        if data["length"] is not None:
            length = data["length"]
            self.length = time(
                hour=length["hour"],
                minute=length["minute"],
                second=length["second"]
            )


class AlbumItem(Item):
    def __init__(
        self,
        release_year: Optional[int] = None,
        length: Optional[time] = None,
        tracks_num: Optional[int] = None,
        artist_items: Optional[List[ArtistItem]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.tracks_num = tracks_num
        self.release_year = release_year
        self.artist_items = artist_items

    def __str__(self) -> str:
        return (
            super().__str__()[:-1] + 
            f", release_year={self.release_year}"
            f", artist_items={self.artist_items}"
            f", length={self.length}"
            f", tracks_num={self.tracks_num}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, AlbumItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.length == __value.length
                and self.tracks_num == __value.tracks_num
                and self.release_year == __value.release_year
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
            self.length,
            self.tracks_num,
            self.release_year,
            self.artist_items,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.ALBUM.value,
            "tracks_num": self.tracks_num,
            "release_year": self.release_year,
            "artist_items": [a.dump() for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.tracks_num = data["tracks_num"]
        self.release_year = data["release_year"]
        self.artist_items = utils.get_artist_items(data["artist_items"])
        if data["length"] is not None:
            length = data["length"]
            self.length = time(
                hour=length["hour"],
                minute=length["minute"],
                second=length["second"]
            )


class EPItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.EP.value
        })
        return d


class PlaylistItem(AlbumItem):
    def __init__(self, views: Optional[int] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.views = views

    def __str__(self) -> str:
        return super().__str__()[:-1] + f", views={self.views}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PlaylistItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.views == __value.views
                and self.length == __value.length
                and self.tracks_num == __value.tracks_num
                and self.release_year == __value.release_year
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
            self.views,
            self.length,
            self.tracks_num,
            self.release_year,
            self.artist_items,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.PLAYLIST.value,
            "views": self.views
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.views = data["views"]


class SingleItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.SINGLE.value
        })
        return d


class SongItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        reproductions: Optional[int] = None,
        album_item: Optional[AlbumItem] = None,
        artist_items: Optional[List[ArtistItem]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.reproductions = reproductions
        self.album_item = album_item
        self.artist_items = artist_items

    def __str__(self) -> str:
        return (
            super().__str__()[:-1] + 
            f", length={self.length}"
            f", reproductions={self.reproductions}"
            f", album_item={self.album_item}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SongItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.length == __value.length
                and self.reproductions == __value.reproductions
                and self.album_item == __value.album_item
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
            self.name,
            self.thumbnail_url,
            self.endpoint,
            self.description,
            self.reproductions,
            self.length,
            self.album_item,
            self.artist_items,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.SONG.value,
            "reproductions": self.reproductions,
            "album_item": self.album_item.dump() if self.album_item else None,
            "artist_items": [a.dump() for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.reproductions = data["reproductions"]
        self.album_item = data["album_item"]
        self.artist_items = utils.get_artist_items(data["artist_items"])
        if data["length"] is not None:
            length = data["length"]
            self.length = time(
                hour=length["hour"],
                minute=length["minute"],
                second=length["second"]
            )


class ProfileItem(Item):
    def __init__(self, handle: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.handle = handle

    def __str__(self) -> str:
        return super().__str__()[:-1] + f", handle={self.handle}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ProfileItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.handle == __value.handle
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.handle,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.PROFILE.value,
            "handle": self.handle
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.handle = data["handle"]


class PodcastItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        artist_items: Optional[List[ArtistItem]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.artist_items = artist_items

    def __str__(self):
        return (
            super().__str__()[:-1] + 
            f", length={self.length}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PodcastItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.length == __value.length
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.length,
                self.artist_items,
            )
        )

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.PODCAST.value,
            "artist_items": [a.dump for a in self.artist_items],
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_artist_items(data["artist_items"])
        if data["length"] is not None:
            length = data["length"]
            self.length = time(
                hour=length["hour"],
                minute=length["minute"],
                second=length["second"]
            )


class EpisodeItem(Item):
    def __init__(
        self,
        publication_date: Optional[date] = None,
        length: Optional[time] = None,
        artist_items: Optional[List[ArtistItem]] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.publication_date = publication_date
        self.artist_items = artist_items

    def __str__(self):
        return (
            super().__str__()[:-1] + f", publication_date={self.publication_date}"
            f", length={self.length}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EpisodeItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.length == __value.length
                and self.artist_items == __value.artist_items
                and self.publication_date == __value.publication_date
            )
        else:
            return False

    def __hash__(self) -> int:
        return hash((
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.length,
                self.artist_items,
                self.publication_date,
        ))

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ItemType.EPISODE.value,
            "artist_items": [a.dump() for a in self.artist_items],
            "publication_date": None if self.publication_date is None else {
                "month": self.publication_date.month,
                "day": self.publication_date.day,
                "year": self.publication_date.year
            },
            "length": None if self.length is None else {
                "hour": self.length.hour,
                "minute": self.length.minute,
                "second": self.length.second
            }
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.artist_items = utils.get_artist_items(data["artist_items"])
        if data["publication_date"] is not None:
            publication_date = data["publication_date"]
            self.publication_date = date(
                month=publication_date["month"],
                day=publication_date["day"],
                year=publication_date["year"]
            )
        if data["length"] is not None:
            length = data["length"]
            self.length = time(
                hour=length["hour"],
                minute=length["minute"],
                second=length["second"]
            )
