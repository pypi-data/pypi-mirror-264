# -*- coding: utf-8 -*-
# Crunchyroll
# Copyright (C) 2024 MrKrabat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json, re, logging
from json import dumps

from typing import Dict, Union, List

from model import CrunchyrollError, ListableItem, EpisodeData, SeriesData, SeasonData
from api import API
from account import Account

# @todo we could change the return type and along with the listables return additional data that we preload
#       like info what is on watchlist, artwork, playhead, ...
#       for that we should use async requests (asyncio)
def get_listables_from_response(account: Account, data: Dict) -> List[ListableItem]:
    """ takes an API response object, determines type of its contents and creates DTOs for further processing """

    listable_items = []

    for item in data:

        if account.mode == 'season':
            listable_items.append(SeasonData(item))
            continue

        if account.mode == 'seasons':
            listable_items.append(SeasonData(item))
            continue

        # fetch type, which is always somewhere else, depending on api endpoint *sighs*
        item_type = item.get('panel', {}).get('type') or item.get('type') or item.get('__class__')
        if not item_type:
            crunchy_log(
                None,
                "get_listables_from_response | failed to determine type for response item %s" % (json.dumps(item, indent=4)),
                logging.ERROR
            )
            continue

        if item_type == 'series':
            listable_items.append(SeriesData(item))
        elif item_type == 'episode':
            listable_items.append(EpisodeData(item))
        else:
            crunchy_log(
                None,
                "get_listables_from_response | unhandled index for metadata. %s" % (json.dumps(item, indent=4)),
                logging.ERROR
            )
            continue

    return listable_items


def get_series_data_from_series_ids(account: Account, api: API, ids: list) -> dict:
    """ fetch info from api object endpoint for given ids. Useful to complement missing data """

    req = api.make_request(
        method="GET",
        url=api.OBJECTS_BY_ID_LIST_ENDPOINT.format(','.join(ids)),
        params={
            "locale": account.subtitle,
            # "preferred_audio_language": ""
        }
    )
    if not req or "error" in req:
        return {}

    return {item.get("id"): item for item in req.get("data")}


def get_stream_id_from_item(item: Dict) -> Union[str, None]:
    """ takes a URL string and extracts the stream ID from it """

    pattern = '/videos/([^/]+)/streams'
    stream_id = re.search(pattern, item.get('__links__', {}).get('streams', {}).get('href', ''))
    # history data has the stream_id at a different location
    if not stream_id:
        stream_id = re.search(pattern, item.get('streams_link', ''))

    if not stream_id:
        raise CrunchyrollError('Failed to get stream id')

    return stream_id[1]


def get_playheads_from_api(account: Account, api: API, episode_ids: Union[str, list]) -> Dict:
    """ Retrieve playhead data from API for given episode / movie ids """

    if isinstance(episode_ids, str):
        episode_ids = [episode_ids]

    response = api.make_request(
        method='GET',
        url=api.PLAYHEADS_ENDPOINT.format(api.account_data.account_id),
        params={
            'locale': account.subtitle,
            'content_ids': ','.join(episode_ids)
        }
    )

    out = {}

    if not response:
        return out

    # prepare by id
    for item in response.get('data'):
        out[item.get('content_id')] = {
            'playhead': item.get('playhead'),
            'fully_watched': item.get('fully_watched')
        }

    return out


def get_image_from_struct(item: Dict, image_type: str, depth: int = 2) -> Union[str, None]:
    """ dive into API info structure and extract requested image from its struct """

    # @todo: add option to specify quality / max size
    if item.get("images") and item.get("images").get(image_type):
        src = item.get("images").get(image_type)
        for i in range(0, depth):
            if src[-1]:
                src = src[-1]
            else:
                return None
        if src.get('source'):
            return src.get('source')

    return None

def dump(data) -> None:
    crunchy_log(dumps(data, indent=4), logging.INFO)

def crunchy_log(account, message, loglevel=logging.INFO, filename = 'crunchy.log') -> None:
    addon_name = account.addon_name if account is not None and hasattr(account, 'addon_name') else "Crunchyroll"
    text= "%s: %s" % (addon_name, str(message))

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=loglevel, encoding='utf-8',
                       format="%(asctime)s [%(levelname)s] %(message)s",
                       handlers=[ logging.FileHandler(filename), logging.StreamHandler()])

    if loglevel ==  logging.DEBUG:
            logger.debug(text)
    if loglevel ==  logging.INFO:
            logger.info(text)
    if loglevel ==  logging.WARNING:
            logger.warning(text)
    if loglevel ==  logging.ERROR:
            logger.error(text)

def convert_subtitle_index_to_string(subtitle_index: int) -> str:
    if subtitle_index == "0":
        return "en-US"
    elif subtitle_index == "1":
        return "en-GB"
    elif subtitle_index == "2":
        return "es-419"
    elif subtitle_index == "3":
        return "es-ES"
    elif subtitle_index == "4":
        return "pt-BR"
    elif subtitle_index == "5":
        return "pt-PT"
    elif subtitle_index == "6":
        return "fr-FR"
    elif subtitle_index == "7":
        return "de-DE"
    elif subtitle_index == "8":
        return "ar-ME"
    elif subtitle_index == "9":
        return "it-IT"
    elif subtitle_index == "10":
        return "ru-RU"
    elif subtitle_index == "11":
        return ""
    else:
        return "en-US"


def filter_seasons(account: Account, item: Dict) -> bool:
    """ takes an API info struct and returns if it matches user language settings """

    # is it a dub in my main language?
    if account.subtitle == item.get('audio_locale', ""):
        return True

    # is it a dub in my alternate language?
    if account.subtitle_fallback and account.subtitle_fallback == item.get('audio_locale', ""):
        return True

    # is it japanese audio, but there are subtitles in my main language?
    if item.get("audio_locale") == "ja-JP":
        # fix for missing subtitles in data
        if item.get("subtitle_locales", []) == [] and item.get('is_subbed', False) is True:
            return True

        if account.subtitle in item.get("subtitle_locales", []):
            return True

        if account.subtitle_fallback and account.subtitle_fallback in item.get("subtitle_locales", []):
            return True

    return False


def get_in_queue(account: Account, api: API, ids: list) -> list:
    """ retrieve watchlist status for given media ids """

    req = api.make_request(
        method="GET",
        url=api.WATCHLIST_V2_ENDPOINT.format(api.account_data.account_id),
        params={
            "content_ids": ','.join(ids),
            "locale": account.subtitle
        }
    )

    if not req or req.get("error") is not None:
        crunchy_log(account, "get_in_queue: Failed to retrieve data", logging.ERROR)
        return []

    if not req.get('data'):
        return []

    return [item.get('id') for item in req.get('data')]

