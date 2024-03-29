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
import re, logging, time
from json import dumps
from datetime import datetime
from typing import Dict, Union

from model import CrunchyrollError,ListableItem
from crunchyrollapi import CrunchyrollAPI, CrunchyrollSettings

def get_series_data_from_series_ids(crunchyroll_settings: CrunchyrollSettings, api: CrunchyrollAPI, ids: list) -> dict:
    """ fetch info from api object endpoint for given ids. Useful to complement missing data """

    req = api.make_request(
        method="GET",
        url=api.OBJECTS_BY_ID_LIST_ENDPOINT.format(','.join(ids)),
        params={
            "locale": crunchyroll_settings.subtitle,
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


def get_playheads_from_api(crunchyroll_settings: CrunchyrollSettings, api: CrunchyrollAPI, episode_ids: Union[str, list]) -> Dict:
    """ Retrieve playhead data from API for given episode / movie ids """

    if isinstance(episode_ids, str):
        episode_ids = [episode_ids]

    response = api.make_request(
        method='GET',
        url=api.PLAYHEADS_ENDPOINT.format(api.account_data.account_id),
        params={
            'locale': crunchyroll_settings.subtitle,
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

def crunchy_dump(crunchyroll_settings, data) -> None:
    crunchy_err(crunchyroll_settings, dumps(data, indent=4))

def crunchy_log(crunchyroll_settings, message, loglevel=logging.INFO, filename = 'crunchy.log') -> None:
    addon_name = crunchyroll_settings.addon_name if crunchyroll_settings is not None and hasattr(crunchyroll_settings, 'addon_name') else "Crunchyroll"
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

def crunchy_info(crunchyroll_settings, message, filename = 'crunchy.log') -> None:
    crunchy_log(crunchyroll_settings, message, loglevel=logging.INFO, filename = filename)

def crunchy_debug(crunchyroll_settings, message, filename = 'crunchy.log') -> None:
    crunchy_log(crunchyroll_settings, message, loglevel=logging.DEBUG, filename = filename)

def crunchy_warn(crunchyroll_settings, message, filename = 'crunchy.log') -> None:
    crunchy_log(crunchyroll_settings, message, loglevel=logging.WARN, filename = filename)

def crunchy_err(crunchyroll_settings, message, filename = 'crunchy.log') -> None:
    crunchy_log(crunchyroll_settings, message, loglevel=logging.ERROR, filename = filename)


def filter_seasons(crunchyroll_settings: CrunchyrollSettings, item: Dict) -> bool:
    """ takes an API info struct and returns if it matches user language settings """

    # is it a dub in my main language?
    if crunchyroll_settings.subtitle == item.get('audio_locale', ""):
        return True

    # is it a dub in my alternate language?
    if crunchyroll_settings.subtitle_fallback and crunchyroll_settings.subtitle_fallback == item.get('audio_locale', ""):
        return True

    # is it japanese audio, but there are subtitles in my main language?
    if item.get("audio_locale") == "ja-JP":
        # fix for missing subtitles in data
        if item.get("subtitle_locales", []) == [] and item.get('is_subbed', False) is True:
            return True

        if crunchyroll_settings.subtitle in item.get("subtitle_locales", []):
            return True

        if crunchyroll_settings.subtitle_fallback and crunchyroll_settings.subtitle_fallback in item.get("subtitle_locales", []):
            return True

    return False


def get_in_queue(crunchyroll_settings: CrunchyrollSettings, api: CrunchyrollAPI, ids: list) -> list:
    """ retrieve watchlist status for given media ids """

    req = api.make_request(
        method="GET",
        url=api.WATCHLIST_V2_ENDPOINT.format(api.account_data.account_id),
        params={
            "content_ids": ','.join(ids),
            "locale": crunchyroll_settings.subtitle
        }
    )

    if not req or req.get("error") is not None:
        crunchy_log(crunchyroll_settings, "get_in_queue: Failed to retrieve data", logging.ERROR)
        return []

    if not req.get('data'):
        return []

    return [item.get('id') for item in req.get('data')]

def debug(crunchyroll_settings, _list, argv):
    text = ""
    for item in _list:
        if issubclass(type(item), ListableItem):
            if argv.field is not None and not argv.field.__len__():
                crunchy_info(crunchyroll_settings, "list available keys : " + str(item.get_keys()))
                exit(0)
            _text = item.get_info(argv.field)
            if _text:
                text+="\n" + str(_text)
            else:
                crunchy_err(crunchyroll_settings, "list available keys : " + str(item.get_keys()))
                exit(15)

    crunchy_info(crunchyroll_settings, text)

def check_arg(crunchyroll_settings, api: CrunchyrollAPI, argv):
    """Run mode-specific functions
        list categories
        search item by categories
        list seasons
        get anime/season
        get search/type 
        get episodes/season
        get history
        get playlist
        get crunchylists
    """
    if argv.category_filter is not None:
        filter_categories = api.list_categories()
        if argv.category_filter in filter_categories:
            return api.search_items_by_category(argv.category_filter)
        else:
            return filter_categories

    if argv.season_filter is not None:
        filter_season = api.list_seasons()
        if argv.season_filter in filter_season:
            return api.search_items_by_season(argv.season_filter)
        else:
            return filter_season
        
    if argv.season_id is not None or \
        argv.id is not None and argv.search_type == "season":
        return api.search_item_by_season_id(argv.season_id)

    if argv.id is not None and argv.search_type == 'series':
        return api.search_season_by_series_id()

    if argv.search is not None:
        return api.search_items_by_string()

    if argv.crunchylist_filter is not None:
        filter_crunchylists = api.list_crunchylists()
        if argv.crunchylist_filter in filter_crunchylists:
            return api.search_items_by_crunchylist()
        else:
            crunchy_info(crunchyroll_settings, "list crunchylist filter %s" % str(filter_crunchylists))
            return filter_crunchylists

    if argv.playlist:
        return api.get_playlist()

    crunchy_err(crunchyroll_settings, "Missing arg defined")
    return None


def date_to_str(date: datetime) -> str:
    return "{}-{}-{}T{}:{}:{}Z".format(
        date.year, date.month,
        date.day, date.hour,
        date.minute, date.second
    )

def str_to_date(string: str) -> datetime:
    time_format = "%Y-%m-%dT%H:%M:%SZ"

    try:
        res = datetime.strptime(string, time_format)
    except TypeError:
        res = datetime(*(time.strptime(string, time_format)[0:6]))

    return res