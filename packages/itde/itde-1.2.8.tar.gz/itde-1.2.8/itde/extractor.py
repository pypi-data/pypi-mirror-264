# type: ignore

import logging

from typing import Optional
from typing import Union
from typing import List
from typing import Callable
from typing import Dict

from .utils import convert_length
from .utils import convert_publication_date
from .utils import convert_number
from .utils import get_item_type

from .endpoints import Endpoint
from .endpoints import BrowseEndpoint
from .endpoints import WatchEndpoint
from .endpoints import UrlEndpoint
from .endpoints import SearchEndpoint

from .containers import CardShelf
from .containers import Shelf
from .containers import Container

from .exceptions import EndpointNotFound
from .exceptions import ITDEError
from .exceptions import UnregisteredItemType
from .exceptions import KeyNotFound
from .exceptions import UnexpectedState

from .items import Item
from .items import AlbumItem
from .items import VideoItem
from .items import ArtistItem
from .items import PlaylistItem
from .items import SongItem
from .items import SingleItem
from .items import EPItem
from .items import PodcastItem
from .items import ProfileItem
from .items import EpisodeItem

from .types import ContinuationStrucType
from .types import ItemStructType
from .types import ShelfStructType
from .types import ResultStructType
from .types import EndpointType
from .types import ItemType


log = logging.getLogger(__name__)


def extract(data: Dict) -> Container:
    if not isinstance(data, Dict):
        raise TypeError("The specified input must be a dict")
    try:
        header = _extract_item(data["header"]) if "header" in data else None
        data_contents = _extract_contents(data)
        container = Container(header=header, contents=None)
        if data_contents is None:
            return container
        contents: List[Shelf] = []
        for entry in data_contents:
            shelf = _extract_shelf(entry)
            if shelf is not None:
                contents.append(shelf)
        container.contents = contents
        return container
    except (KeyError, IndexError, TypeError, ValueError, ITDEError) as error:
        log.debug(
            "An error occurred during the data extraction process. "
            "Please open an issue at https://github.com/g3nsy/itde/issues"
        )
        raise ITDEError(
            "An error occurred during the data extraction process: "
            f"{error.__class__.__name__}: "
            f"{error.args[0] if error.args else ''}. "
            f"Please open an issue at https://github.com/g3nsy/itde/issues"
        ) from error


def _extract_contents(data: Dict) -> Optional[Union[Dict, List]]:
    if ContinuationStrucType.CONTINUATION.value in data:
        key = ContinuationStrucType.CONTINUATION.value

        if ContinuationStrucType.SECTION_LIST.value in data[key]:
            contents = data[key][ContinuationStrucType.SECTION_LIST.value]["contents"]

        elif ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value in data[key]:
            contents = [
                {
                    ShelfStructType.MUSIC_SHELF.value: data[key][
                        ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value
                    ]
                }
            ]

        elif ContinuationStrucType.MUSIC_SHELF.value in data[key]:
            contents = [
                {
                    ShelfStructType.MUSIC_SHELF.value: data[key][
                        ContinuationStrucType.MUSIC_SHELF.value
                    ]
                }
            ]

        else:
            raise UnexpectedState()

    elif ResultStructType.TWO_COLUMN_BROWSE_RESULT.value in data["contents"]:
        contents = data["contents"][ResultStructType.TWO_COLUMN_BROWSE_RESULT.value][
            "secondaryContents"]["sectionListRenderer"]["contents"]

    elif ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value in data["contents"]:
        tmp = data["contents"][ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value][
                "tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]

        if ShelfStructType.GRID.value in tmp["contents"][0]:
            contents = tmp["contents"]

        elif ShelfStructType.MUSIC_PLAYLIST_SHELF.value in tmp["contents"][0]:
            contents = tmp["contents"][0]["musicPlaylistShelfRenderer"]["contents"]

        elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in tmp["contents"][0]:
            contents = tmp["contents"]

        elif ShelfStructType.MUSIC_SHELF.value in tmp["contents"][0]:
            contents = tmp["contents"]

        else:
            raise UnexpectedState()

    elif ResultStructType.TABBED_SEARCH_RESULTS.value in data["contents"]:
        contents = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0][
            "tabRenderer"]["content"]["sectionListRenderer"]["contents"]

    elif ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in data["contents"]:
        try:
            contents = [
                data["contents"][ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value][
                    "tabbedRenderer"]["watchNextTabbedResultsRenderer"]["tabs"][0][
                    "tabRenderer"]["content"]["musicQueueRenderer"]["content"]
            ]
        except KeyError:
            contents = None
    else:
        raise KeyNotFound(data["contents"].keys())

    return contents


def _extract_shelf(entry: Dict) -> Optional[Shelf]:
    if ShelfStructType.MUSIC_SHELF.value in entry:
        key = ShelfStructType.MUSIC_SHELF.value
        try:
            name = entry[key]["title"]["runs"][0]["text"]
        except KeyError:
            name = None
        try:
            endpoint = _extract_endpoint(data=entry[key]["bottomEndpoint"])
        except KeyError:
            endpoint = None
        entry_contents = entry[key]["contents"]
        try:
            continuation = entry[key]["continuations"][0][
                "nextContinuationData"]["continuation"]
        except (IndexError, KeyError):
            continuation = None
        shelf = Shelf(
            name=name, endpoint=endpoint, continuation=continuation,
        )
    elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CAROUSEL_SHELF.value
        entry_contents = entry[key]["contents"]
        name = entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"][
            "title"]["runs"][0]["text"]
        try:
            endpoint = _extract_endpoint(
                data=entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                    "title"]["runs"][0]["navigationEndpoint"]
            )
        except KeyError:
            endpoint = None
        shelf = Shelf(
            name=name, endpoint=endpoint, continuation=None
        )
    elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        entry_contents = entry[key].get("contents", [])
        item = _extract_item(entry)
        if item:
            shelf = CardShelf(item=item)
        else:
            return None
    elif ShelfStructType.PLAYLIST_PANEL.value in entry:
        key = ShelfStructType.PLAYLIST_PANEL.value
        name = entry[key].get("title", None)
        entry_contents = entry[key]["contents"]
        shelf = Shelf(
            name=name, endpoint=None, continuation=None
        )
    elif ShelfStructType.GRID.value in entry:
        key = ShelfStructType.GRID.value
        shelf = Shelf()
        entry_contents = entry[key]["items"]
    elif (
        ShelfStructType.ITEM_SECTION.value in entry or
        ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry
    ):
        return None
    else:
        raise KeyNotFound(entry.keys())

    item_type = get_item_type(shelf.name) if shelf.name else None
    for entry_item in entry_contents:
        item = _extract_item(entry_item, item_type)
        if item:
            shelf.append(item)
    return shelf


def _extract_item(entry_item: Dict, item_type: Optional[ItemType] = None) -> Optional[Item]:
    if ShelfStructType.MUSIC_CARD_SHELF.value in entry_item:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        try:
            item_type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
        except ValueError:
            return None
        name = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(
            entry_item[key]["title"]["runs"][0]["navigationEndpoint"]
        )
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        match item_type:
            case ItemType.ALBUM:
                item = AlbumItem(
                    # artist_items in entry[key]['subtitle'][1:]
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                )
            case ItemType.ARTIST:
                subscribers = convert_number(
                    entry_item[key]["subtitle"]["runs"][-1]["text"]
                )
                item = ArtistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )
            case ItemType.VIDEO:
                # artist_items in entry_item[key]['subtitle']['runs'][2:-3]
                views = convert_number(entry_item[key]["subtitle"]["runs"][-3]["text"])
                length = convert_length(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = VideoItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    views=views,
                    length=length,
                )
            case ItemType.EP:
                # artist_items in entry[key]['subtitle'][2:]
                item = EPItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                )
            case ItemType.SONG:
                length = convert_length(entry_item[key]["subtitle"]["runs"][-1]["text"])
                album_item = AlbumItem(
                    name=entry_item[key]["subtitle"]["runs"][-3]["text"],
                    thumbnail_url=thumbnail_url,
                    endpoint=_extract_endpoint(
                        entry_item[key]["subtitle"]["runs"][-3]["navigationEndpoint"]
                    ),
                )
                item = SongItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    album_item=album_item,
                )
            case ItemType.EPISODE:
                # TODO artist_items in entry[key][subtitle][runs][4:]
                try:
                    publication_date = convert_publication_date(
                        string=entry_item[key]["subtitle"]["runs"][2]
                    )
                except UnexpectedState:
                    publication_date = None
                item = EpisodeItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    publication_date=publication_date,
                )
            case _:
                raise UnregisteredItemType(item_type)

    elif ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
        try:
            thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
                "thumbnail"]["thumbnails"][-1]["url"]
        except KeyError:
            thumbnail_url = None
        name = entry_item[key]["flexColumns"][0][
            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
        if item_type is None:
            try:
                item_type = ItemType(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"][
                        "runs"][0]["text"]
                )
            except (KeyError, ValueError):
                item_type = ItemType.SONG
        match item_type:
            case ItemType.ARTIST:
                try:
                    subscribers = convert_number(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except UnexpectedState:
                    subscribers = None
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = ArtistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )
            case ItemType.ALBUM:
                release_year = int(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["text"]
                )
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = AlbumItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )
            case ItemType.VIDEO:
                length = convert_length(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["text"]
                )
                views = convert_number(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-3]["text"]
                )
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = VideoItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    views=views,
                )
            case ItemType.PLAYLIST:
                try:
                    tracks_num = int(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    tracks_num = None
                try:
                    views = convert_number(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    views = None
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = PlaylistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    views=views,
                )
            case ItemType.SINGLE:
                release_year = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = SingleItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year),
                )
            case ItemType.SONG:
                try:
                    length = convert_length(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (UnexpectedState, KeyError):
                    length = None
                try:
                    reproductions = convert_number(
                        entry_item[key]["flexColumns"][-1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (UnexpectedState, KeyError):
                    try:
                        reproductions = convert_number(
                            entry_item[key]["flexColumns"][-2][
                                "musicResponsiveListItemFlexColumnRenderer"][
                                "text"]["runs"][-1]["text"]
                        )
                    except (UnexpectedState, KeyError):
                        reproductions = None
                try:
                    endpoint = _extract_endpoint(
                        data=entry_item[key]["flexColumns"][0][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["navigationEndpoint"]
                    )
                except KeyError:
                    endpoint = None
                item = SongItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    reproductions=reproductions,
                    album_item=None,
                )
            case ItemType.EPISODE:
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = EpisodeItem(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url,
                )
            case ItemType.PODCAST:
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = PodcastItem(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url
                )
            case ItemType.PROFILE:
                item_handle = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                item = ProfileItem(
                    name=name, thumbnail_url=thumbnail_url, handle=item_handle,
                )
            case ItemType.EP:
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = EPItem(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url,
                )
            case _:
                raise UnregisteredItemType(item_type)
    elif ItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_TWO_ROW_ITEM.value
        thumbnail_url = entry_item[key]["thumbnailRenderer"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        name = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])

        if item_type is None:
            try:
                item_type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
            except ValueError:
                item_type = None
        match item_type:
            case ItemType.ARTIST:
                subscribers = convert_number(
                    entry_item[key]["subtitle"]["runs"][0]["text"]
                )
                item = ArtistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )
            case ItemType.ALBUM:
                try:
                    release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                except ValueError:
                    release_year = None
                item = AlbumItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )
            case ItemType.EP:
                try:
                    release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                except ValueError:
                    release_year = None
                item = EPItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )
            case ItemType.VIDEO:
                views = convert_number(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = VideoItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    views=views,
                )
            case ItemType.PLAYLIST:
                item = PlaylistItem(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url,
                )
            case ItemType.SINGLE:
                try:
                    release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                except ValueError:
                    release_year = None
                item = SingleItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )
            case ItemType.SONG:
                item = SongItem(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url,
                )
            case ItemType.EPISODE | ItemType.PODCAST | ItemType.PROFILE:
                raise UnexpectedState(item_type)
            case _:
                item = Item(
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url,
                )
    elif ItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
        key = ItemStructType.PLAYLIST_PANEL_VIDEO.value
        name = entry_item[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(entry_item[key]["navigationEndpoint"])
        length = convert_length(entry_item[key]["lengthText"]["runs"][-1]["text"])
        thumbnail_url = entry_item[key]["thumbnail"]["thumbnails"][-1]["url"]

        tmp = entry_item[key]["thumbnail"]["thumbnails"][-1]
        width, height = tmp["width"], tmp["height"]
        if width / height == 1:
            item = SongItem(
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                album_item=None,
            )
        else:
            try:
                views = convert_number(
                    entry_item[key]["longBylineText"]["runs"][-3]["text"]
                )
            except (KeyError, IndexError):
                views = None
            item = VideoItem(
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                views=views,
            )
    elif ItemStructType.MUSIC_IMMERSIVE_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_IMMERSIVE_HEADER.value
        try:
            description = entry_item[key]["description"]["runs"][0]["text"]
        except KeyError:
            description = None
        item = ArtistItem(
            name=entry_item[key]["title"]["runs"][0]["text"],
            description=description,
            thumbnail_url=entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
                "thumbnail"]["thumbnails"][-1]["url"],
            subscribers=entry_item[key]["subscriptionButton"][
                "subscribeButtonRenderer"]["subscriberCountText"]["runs"][0]["text"],
            endpoint=None,
        )
    elif ItemStructType.MUSIC_DETAIL_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_DETAIL_HEADER.value
        item_type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
        name = entry_item[key]["title"]["runs"][0]["text"]
        thumbnail_url = entry_item[key]["thumbnail"]["croppedSquareThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
        if item_type is ItemType.PLAYLIST:
            tracks_num = entry_item[key]["secondSubtitle"]["runs"][2]["text"]
        else:
            tracks_num = entry_item[key]["secondSubtitle"]["runs"][0]["text"]
        # TODO artist_items
        match item_type:
            case ItemType.ALBUM:
                item = AlbumItem(
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )
            case ItemType.EP:
                item = EPItem(
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )
            case ItemType.SINGLE:
                item = SingleItem(
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )
            case ItemType.PLAYLIST:
                views = convert_number(
                    entry_item[key]["secondSubtitle"]["runs"][0]["text"]
                )
                item = PlaylistItem(
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                    views=views,
                )
            case _:
                raise UnexpectedState(item_type)
    elif ItemStructType.MUSIC_VISUAL_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_VISUAL_HEADER.value
        name = entry_item[key]["title"]["runs"][-1]["text"]
        # TODO foreground thumbnail
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        item = Item(
            name=name, thumbnail_url=thumbnail_url,
        )
    elif ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value
        name = entry_item[key]["title"]["runs"][0]["text"]
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        endpoint = _extract_endpoint(
            entry_item[key]["title"]["runs"][0]["navigationEndpoint"]
        )
        item = Item(
            name=name, thumbnail_url=thumbnail_url, endpoint=endpoint
        )
    elif (
        ItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry_item or
        ItemStructType.PLAYLIST_EXPANDABLE_MESSAGE.value in entry_item or
        ItemStructType.MESSAGE.value in entry_item
    ):
        return None
    else:
        raise KeyNotFound(f"Content: {entry_item.keys()}")

    return item


def _extract_endpoint(data: Dict) -> Endpoint:
    if EndpointType.BROWSE.value in data:
        endpoint_data = data["browseEndpoint"]
        browse_id = endpoint_data["browseId"]
        endpoint = BrowseEndpoint(
            browse_id=browse_id, params=endpoint_data.get("params", None)
        )
    elif EndpointType.WATCH.value in data:
        endpoint_data = data["watchEndpoint"]
        video_id = endpoint_data["videoId"]
        endpoint = WatchEndpoint(
            video_id=video_id,
            playlist_id=endpoint_data.get("playlist_id", None),
            params=endpoint_data.get("params", None),
        )
    elif EndpointType.SEARCH.value in data:
        endpoint_data = data["searchEndpoint"]
        query = endpoint_data["query"]
        endpoint = SearchEndpoint(
            query=query, params=endpoint_data.get("params", None)
        )
    elif EndpointType.URL in data:
        endpoint_data = data["urlEndpoint"]
        url = endpoint_data["url"]
        endpoint = UrlEndpoint( 
            url=url, params=endpoint_data.get("params", None)
        )
    else:
        raise EndpointNotFound(f"Endpoint not found in: {data}")
    return endpoint
