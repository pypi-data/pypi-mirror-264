# type: ignore
import re
from typing import Callable, Optional, List, Dict
from datetime import time, date
from .items import Item
from .items import ArtistItem
from .items import VideoItem
from .items import AlbumItem
from .items import EPItem
from .items import PlaylistItem
from .items import SingleItem
from .items import SongItem
from .items import ProfileItem
from .items import PodcastItem
from .items import EpisodeItem
from .types import EndpointType, ItemType
from .exceptions import UnexpectedState
from .endpoints import WatchEndpoint
from .endpoints import BrowseEndpoint
from .endpoints import UrlEndpoint
from .endpoints import SearchEndpoint
from .endpoints import Endpoint


def handle(function: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, ValueError, IndexError, TypeError) as error:
            raise UnexpectedState(
                f"Unexpected state detected: {error.args[0]}"
            ) from error

    return inner_function


@handle
def convert_number(string: str) -> int:
    _match = re.search(r"(\d+\.\d+|\d+)([BMK])?", string)
    result = _match.group() if _match else ""
    last_char = result[-1]
    if last_char.isupper():
        number = float(result[:-1])
        match last_char:
            case "B":
                factor = 1000000000
            case "M":
                factor = 1000000
            case "K":
                factor = 1000
            case _:
                raise ValueError(f"Unexpected character: {last_char}")
        return int(number * factor)
    else:
        return int(result)


@handle
def convert_length(string: str) -> time:
    time_list = [int(x) for x in string.split(":")]
    match len(time_list):
        case 3:
            return time(hour=time_list[0], minute=time_list[1], second=time_list[2])
        case 2:
            return time(minute=time_list[0], second=time_list[1])
        case _:
            raise ValueError(f"Unexpected time format: {string}")


@handle
def convert_publication_date(string: str) -> date:
    month, day, year = string.split()
    return date(month=convert_month(month), day=int(day[:-1]), year=int(year))


@handle
def convert_month(month: str) -> int:
    match month.lower():
        case "jan":
            return 1
        case "feb":
            return 2
        case "mar":
            return 3
        case "apr":
            return 4
        case "may":
            return 5
        case "jun":
            return 6
        case "jul":
            return 7
        case "aug":
            return 8
        case "sep":
            return 9
        case "oct":
            return 10
        case "nov":
            return 11
        case "dec":
            return 12
        case _:
            raise ValueError("Unexpected month: {month}")


def get_item_type(shelf_name: str) -> Optional[ItemType]:
    if match("song", shelf_name):
        return ItemType.SONG
    if match("single", shelf_name):
        return ItemType.SINGLE
    if match("video", shelf_name):
        return ItemType.VIDEO
    if match("playlist", shelf_name):
        return ItemType.PLAYLIST
    if match("album", shelf_name):
        return ItemType.ALBUM
    if match("artist", shelf_name):
        return ItemType.ARTIST
    if match("episode", shelf_name):
        return ItemType.EPISODE
    if match("profile", shelf_name):
        return ItemType.PROFILE
    if match("podcast", shelf_name):
        return ItemType.PODCAST
    if match("ep", shelf_name):
        return ItemType.EP
    return None


def match(seq: str, title: str) -> bool:
    return re.search(seq, title, re.IGNORECASE) is not None


def get_artist_items(data: List) -> List[ArtistItem]:
    artist_items = []
    for artist_data in data:
        artist_item = ArtistItem()
        artist_item.load(artist_data)
        artist_items.append(artist_item)
    return artist_items


def get_items(data: List) -> List[Item]:
    return [get_item(item_data) for item_data in data]


def get_item(data: Dict) -> Item:
    match data["type"]:
        case ItemType.ARTIST.value:
            item = ArtistItem()
        case ItemType.VIDEO.value:
            item = VideoItem()
        case ItemType.ALBUM.value:
            item = AlbumItem()
        case ItemType.EP.value:
            item = EPItem()
        case ItemType.PLAYLIST.value:
            item = PlaylistItem()
        case ItemType.SINGLE.value:
            item = SingleItem()
        case ItemType.SONG.value:
            item = SongItem()
        case ItemType.PROFILE.value:
            item = ProfileItem()
        case ItemType.PODCAST.value:
            item = PodcastItem()
        case ItemType.EPISODE.value:
            item = EpisodeItem()
        case None:
            item = Item()
        case _:
            raise ValueError("Invalid type")
    item.load(data)
    return item


def get_endpoint(data: Dict) -> Endpoint:
    match data["type"]:
        case EndpointType.URL.value:
            endpoint = UrlEndpoint()
        case EndpointType.BROWSE.value:
            endpoint = BrowseEndpoint()
        case EndpointType.SEARCH.value:
            endpoint = SearchEndpoint()
        case EndpointType.WATCH.value:
            endpoint = WatchEndpoint()
        case _:
            raise ValueError("Invalid type")
    endpoint.load(data)
    return endpoint
