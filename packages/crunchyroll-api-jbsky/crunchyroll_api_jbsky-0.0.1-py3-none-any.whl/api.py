# Crunchyroll API 
# Use the crunchyroll API with an authenticated premium account
# Copyright (C) 2024 jbsky
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

import os.path, os, logging
import json
import time
from datetime import timedelta, datetime
from typing import Optional, Dict

import requests
from requests import HTTPError, Response

import utils
from typing import Dict, List

from model import AccountData, Account, LoginError, SeasonData, SeriesData, EpisodeData, ListableItem, CrunchyrollError

class API:
    """ Api documentation https://github.com/hyugogirubato/API-Crunchyroll-Beta/wiki/Api """
    URL = "https://api.crunchyroll.com/"
    VERSION = "1.1.21.0"

    INDEX_ENDPOINT = "https://beta-api.crunchyroll.com/index/v2"
    PROFILE_ENDPOINT = "https://beta-api.crunchyroll.com/accounts/v1/me/profile"
    TOKEN_ENDPOINT = "https://beta-api.crunchyroll.com/auth/v1/token"
    SEARCH_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/search"
    STREAMS_ENDPOINT = "https://beta-api.crunchyroll.com/cms/v2{}/videos/{}/streams"
    # SERIES_ENDPOINT = "https://beta-api.crunchyroll.com/cms/v2{}/series/{}"
    SEASONS_ENDPOINT = "https://beta-api.crunchyroll.com/cms/v2{}/seasons"
    EPISODES_ENDPOINT = "https://beta-api.crunchyroll.com/cms/v2{}/episodes"
    OBJECTS_BY_ID_LIST_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/cms/objects/{}"
    # SIMILAR_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/{}/similar_to"
    # NEWSFEED_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/news_feed"
    BROWSE_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/browse"
    # there is also a v2, but that will only deliver content_ids and no details about the entries
    WATCHLIST_LIST_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/{}/watchlist"
    # only v2 will allow removal of watchlist entries.
    # !!!! be super careful and always provide a content_id, or it will delete the whole playlist! *sighs* !!!!
    # WATCHLIST_REMOVE_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/watchlist/{}"
    WATCHLIST_V2_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/watchlist"
    PLAYHEADS_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/playheads"
    HISTORY_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/watch-history"
    RESUME_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/discover/{}/history"
    SEASONAL_TAGS_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/discover/seasonal_tags"
    CATEGORIES_ENDPOINT = "https://beta-api.crunchyroll.com/content/v1/tenant_categories"
    SKIP_EVENTS_ENDPOINT = "https://static.crunchyroll.com/skip-events/production/{}.json"  # request w/o auth req.
    INTRO_V2_ENDPOINT = "https://static.crunchyroll.com/datalab-intro-v2/{}.json"

    CRUNCHYLISTS_LISTS_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/custom-lists"
    CRUNCHYLISTS_VIEW_ENDPOINT = "https://beta-api.crunchyroll.com/content/v2/{}/custom-lists/{}"

    AUTHORIZATION = "Basic bHF0ai11YmY1aHF4dGdvc2ZsYXQ6N2JIY3hfYnI0czJubWE1bVdrdHdKZEY0ZTU2UU5neFQ="

    def __init__(self, account: Account = None, mode = "") -> None:
        self.http = requests.Session()
        self.locale: str = account.subtitle if hasattr(account, "subtitle") else None
        self.mode: str = mode
        self.account_data: AccountData = AccountData(dict())
        self.api_headers: Dict = {
            "User-Agent": "Crunchyroll/3.50.2",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.account = account

    def start(self) -> bool:
        session_restart = self.account.session_restart

        # restore account data from file
        session_data = self.load_from_storage()
        if session_data and not session_restart:
            self.account_data = AccountData(session_data)
            account_auth = {"Authorization": f"{self.account_data.token_type} {self.account_data.access_token}"}
            self.api_headers.update(account_auth)

            # check if tokes are expired
            if datetime.utcnow() > str_to_date(self.account_data.expires):
                session_restart = True
            else:
                return True

        # session management
        self.create_session(session_restart)

        return True

    def create_session(self, refresh=False) -> None:
        headers = {"Authorization": API.AUTHORIZATION}

        if not refresh:
            data = {
                "username": self.account.settings.crunchyroll_username,
                "password": self.account.settings.crunchyroll_password,
                "grant_type": "password",
                "scope": "offline_access",
            }
        else:
            data = {
                "refresh_token": self.account_data.refresh_token,
                "grant_type": "refresh_token",
                "scope": "offline_access",
            }

        r = self.http.request(method="POST", url=API.TOKEN_ENDPOINT, headers=headers, data=data)

        # if refreshing and refresh token is expired, it will throw a 400
        if r.status_code == 400:
            if refresh:
                utils.crunchy_log(self.account, "Invalid/Expired credentials, try restarting session from scratch", logging.INFO)
                self.delete_storage()
                return self.create_session()
            else:
                utils.crunchy_log(self.account, "Failed to authenticate!", logging.ERROR)
                raise LoginError("Failed to authenticate")

        r_json = self.get_json_from_response(r)

        self.api_headers.clear()
        self.api_headers.update({"Authorization": "%s %s" % (r_json["token_type"], r_json["access_token"])})

        account_data = dict()
        account_data.update(r_json)

        # before make_request for refresh account data, we must clear object
        self.account_data = AccountData({})
        r = self.make_request(method="GET", url=API.INDEX_ENDPOINT)
        account_data.update(r)

        r = self.make_request(method="GET", url=API.PROFILE_ENDPOINT)
        account_data.update(r)

        expire = datetime.utcnow() + timedelta(seconds=float(account_data["expires_in"]))
        account_data["expires"] = date_to_str(expire)

        self.account_data = AccountData(account_data)

        self.write_to_storage(self.account_data)

    def close(self) -> None:
        """Saves cookies and session
        """
        # no longer required, data is saved upon session update already

    def destroy(self) -> None:
        """Destroys session
        """
        self.delete_storage()

    def make_request(self, method: str, url: str, headers=dict(), params=dict(), data=None, json_data=None, is_retry=False ) -> Optional[Dict]:
        if self.account_data:
            if expiration := self.account_data.expires:
                if datetime.utcnow() > str_to_date(expiration):
                    self.create_session(refresh=True)
            params.update({
                "Policy": self.account_data.cms.policy,
                "Signature": self.account_data.cms.signature,
                "Key-Pair-Id": self.account_data.cms.key_pair_id
            })
        request_headers = {}
        request_headers.update(self.api_headers)
        request_headers.update(headers)

        r = self.http.request(method, url, headers=request_headers, params=params, data=data, json=json_data)

        # something went wrong with authentication, possibly an expired token that wasn't caught above due to host
        # clock issues. set expiration date to 0 and re-call, triggering a full session refresh.
        if r.status_code == 401:
            if is_retry:
                raise LoginError('Request to API failed twice due to authentication issues.')

            utils.crunchy_log(self.account, "make_request_proposal: request failed due to auth error", logging.ERROR)
            self.account_data.expires = 0
            return self.make_request(method, url, headers, params, data, json_data, True)

        return self.get_json_from_response(r)

    def make_unauthenticated_request(self, method: str, url: str, headers=None, params=None, data=None, json_data=None) -> Optional[Dict]:
        """ Send a raw request without any session information """

        req = requests.Request(method, url, data=data, params=params, headers=headers, json=json_data)
        prepped = req.prepare()
        r = self.http.send(prepped)

        return self.get_json_from_response(r)

    def get_storage_path(self) -> str:
        """Get cookie file path
        """
        return self.account.profile_path

    def load_from_storage(self) -> Optional[Dict]:
        storage_file = self.get_storage_path() + "session_data.json"

        if not os.path.isfile(storage_file):
            return None

        with open(storage_file, 'r') as file:
            data = json.load(file)

        return data

    def delete_storage(self) -> None:
        storage_file = self.get_storage_path() + "session_data.json"

        if not os.path.isfile(storage_file):
            return None

        os.remove(storage_file)

    def write_to_storage(self, account: AccountData) -> bool:
        storage_file = self.get_storage_path() + "session_data.json"

        # serialize (Object has a to_str serializer)
        json_string = str(account)

        with open(storage_file, 'w') as file:
            result = file.write(json_string)

        return result
    
    def list_categories(self, account):
        # api request for category names / tags
        req = self.make_request(
            method="GET",
            url=self.CATEGORIES_ENDPOINT,
            params={ "locale": account.subtitle }
        )

        filter_categories = list()

        for f in req["items"]:
            filter_categories.append(f['tenant_category'])

        return filter_categories

    def search_items_by_category(self, account):
        """ view all anime from selected mode
        """
        category_filter: str = account.category_filter
        params = {
            "locale": account.subtitle,
            "categories": category_filter,
            "n": int(account.items_per_page) or 50,
            "start": int(account.offset) or 0,
            "ratings": 'true'
        }

        # api request
        req = self.make_request(method="GET", url=self.BROWSE_ENDPOINT, params = params)

        self.get_listables_from_response(account, req.get('items'))

    def search_items_by_season(self, account):
        """ view all available anime seasons """

        season_filter = None

        if hasattr(account, "season_filter"):
            season_filter: str = account.season_filter

        params = { "locale": account.subtitle, "season_tag": season_filter, "n": 100}

        req = self.make_request(method = "GET", url = self.BROWSE_ENDPOINT, params = params)

        return self.get_listables_from_response(account, req.get('items'))

    def search_season_by_series_id(self, account):
        """ view all seasons/arcs of an anime """

        if not hasattr(account, 'subtitle'):
            raise CrunchyrollError('subtitle not defined')

        if not hasattr(account, 'id'):
            utils.crunchy_log(account, 'id not defined', logging.ERROR)
            return None
    
        url = self.SEASONS_ENDPOINT.format(self.account_data.cms.bucket)
        params = { "locale": account.subtitle,
                   "series_id": account.id,
                   "preferred_audio_language": self.account_data.default_audio_language,
                   "force_locale": ""
        }
        # api request
        req = self.make_request(method = "GET", url = url, params = params)

        return self.get_listables_from_response(account, req.get('items'))

    def list_seasons(self, account):
        """ view all available seasons """
        params = {"locale": account.subtitle}

        req = self.make_request(method = "GET", url = self.SEASONAL_TAGS_ENDPOINT, params = params )

        filter_season = list()

        for f in req["data"]:
            filter_season.append(f['id'])

        return filter_season
        # return get_listables_from_response(account, req.get('data'))
    
    def search_items_by_string(self, account):
        """ Search for string by type 
            available types seem to be: music,series,episode,top_results,movie_listing
            TODO: Extract all search type
        """

        if not hasattr(account, "offset"):
                account.offset = 0

        url = self.SEARCH_ENDPOINT
        params = {
            "n": 50,
            "q": account.search,
            "locale": account.subtitle,
            "start": int(account.offset) or 0,
            "type": account.search_type
        }

        req = self.make_request(method="GET", url = url, params = params)

        type_data = req.get('items')[0]  # @todo: for now we support only the first type, which should be series
        return self.get_listables_from_response(account, type_data.get('items'))

    def search_item_by_season_id(self, account):
        """ view all episodes of season """

        url = self.EPISODES_ENDPOINT.format(self.account_data.cms.bucket)
        params = { "locale": account.subtitle, "season_id": account.season_id }

        req = self.make_request(method = "GET", url = url, params = params)

        return self.get_listables_from_response(account, req.get('items'))

    def list_item_by_history(self, account):
        """ shows history of watched anime
        """
        items_per_page = 50
        current_page = int(account.offset) or 1

        url = self.HISTORY_ENDPOINT.format(self.account_data.account_id)
        params = { "page_size": items_per_page, "page": current_page, "locale": account.subtitle}
        
        req = self.make_request( method="GET", url = url, params = params)

        return self.get_listables_from_response(account, req.get('data'))

    def list_item_resume(self, account):
        """ shows episode to resume for watching animes
        """
        items_per_page = 50

        if not hasattr(account, "offset"):
                account.offset = 0

        url = self.RESUME_ENDPOINT.format(self.account_data.account_id)
        params = { "n": items_per_page, "locale": account.subtitle, "start": int(account.offset) }

        req = self.make_request(method = "GET", url = url, params = params)

        return self.get_listables_from_response(account, req.get('data'))

    def get_playlist(self, account):
        """ shows anime queue/playlist """
        params = { "n": 1024, "locale": account.subtitle }
        url = self.WATCHLIST_LIST_ENDPOINT.format(self.account_data.account_id)

        req = self.make_request(method = "GET", url = url, params = params)

        return get_listables_from_response(account, req.get('items')),

    def list_crunchylists(self, account):
        """ Retrieve all crunchylists """

        url = self.CRUNCHYLISTS_LISTS_ENDPOINT.format(self.account_data.account_id)
        params = { 'locale': account.subtitle }
        req = self.make_request(method = 'GET', url = url, params = params)

        # check for error
        if not req or 'error' in req:
            return False

        return get_listables_from_response(account, req.get('data'))

    def search_items_by_crunchylist(self, account):
        """ Retrieve all items for a crunchylist """

        utils.crunchy_log(account, "Fetching crunchylist: %s" % account.get('crunchylists_item_id'))
        url = self.CRUNCHYLISTS_VIEW_ENDPOINT.format(self.account_data.account_id, account.crunchylist_item_id)
        params = { 'locale': account.subtitle }

        req = self.make_request(method='GET', url = url, params = params)

        return get_listables_from_response(account, req.get('data'))

    def get_listables_from_response(self, account: Account, data: Dict) -> List[ListableItem]:
        """ takes an API response object, determines type of its contents and creates DTOs for further processing """

        listable_items = []

        for item in data:

            # fetch type, which is always somewhere else, depending on api endpoint *sighs*
            item_type = item.get('panel', {}).get('type') or item.get('type') or item.get('__class__')
            if not item_type:
                utils.crunchy_log(account, "failed to determine type for response item %s"
                                  % (json.dumps(item, indent=4)), logging.ERROR)
                continue

            if item_type == 'series':
                listable_items.append(SeriesData(item))
            elif item_type == 'episode':
                listable_items.append(EpisodeData(item))
            else:
                utils.crunchy_log(account, "unhandled index for metadata. %s"
                                  % (json.dumps(item, indent=4)), logging.ERROR)
                continue

        return listable_items

    def get_json_from_response(self, r: Response) -> Optional[Dict]:

        code: int = r.status_code
        response_type: str = r.headers.get("Content-Type")

        # no content - possibly POST/DELETE request?
        if not r or not r.text:
            try:
                r.raise_for_status()
                return None
            except HTTPError as e:
                # r.text is empty when status code cause raise
                r = e.response

        # handle text/plain response (e.g. fetch subtitle)
        if response_type == "text/plain":
            # if encoding is not provided in the response, Requests will make an educated guess and very likely fail
            # messing encoding up - which did cost me hours. We will always receive utf-8 from crunchy, so enforce that
            r.encoding = "utf-8"
            d = dict()
            d.update({
                'data': r.text
            })
            return d

        if not r.ok and r.text[0] != "{":
            raise CrunchyrollError(f"[{code}] {r.text}")

        try:
            r_json: Dict = r.json()
        except requests.exceptions.JSONDecodeError:
            utils.crunchy_log(self.account, "Failed to parse response data", logging.ERROR)
            return None

        if "error" in r_json:
            error_code = r_json.get("error")
            if error_code == "invalid_grant":
                raise LoginError(f"[{code}] Invalid login credentials.")
        elif "message" in r_json and "code" in r_json:
            message = r_json.get("message")
            raise CrunchyrollError(f"[{code}] Error occurred: {message}")
        if not r.ok:
            raise CrunchyrollError(f"[{code}] {r.text}")

        return r_json

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

