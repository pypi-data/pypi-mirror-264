# -*- coding: utf-8 -*-
# Crunchyroll
# Copyright (C) 2018 MrKrabat
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
from abc import abstractmethod
from typing import Any, Dict, Union

from json import dumps

from account import Account
import utils

class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~hi"})):
    def __str__(self):
        return f"<class 'crunchyroll_beta.types.{self.__name__}'>"


class Object(metaclass=Meta):
    @staticmethod
    def default(obj: "Object"):
        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)


class CMS(Object):
    def __init__(self, data: dict):
        self.bucket: str = data.get("bucket")
        self.policy: str = data.get("policy")
        self.signature: str = data.get("signature")
        self.key_pair_id: str = data.get("key_pair_id")


class AccountData(Object):
    def __init__(self, data: dict):
        self.access_token: str = data.get("access_token")
        self.refresh_token: str = data.get("refresh_token")
        self.expires: str = data.get("expires")
        self.token_type: str = data.get("token_type")
        self.scope: str = data.get("scope")
        self.country: str = data.get("country")
        self.account_id: str = data.get("account_id")
        self.cms: CMS = CMS(data.get("cms", {}))
        self.service_available: bool = data.get("service_available")
        self.avatar: str = data.get("avatar")
        self.has_beta: bool = data.get("cr_beta_opt_in")
        self.email_verified: bool = data.get("crleg_email_verified")
        self.email: str = data.get("email")
        self.maturity_rating: str = data.get("maturity_rating")
        self.account_language: str = data.get("preferred_communication_language")
        self.default_subtitles_language: str = data.get("preferred_content_subtitle_language")
        self.default_audio_language: str = data.get("preferred_content_audio_language")
        self.username: str = data.get("username")


class ListableItem(Object):
    """ Base object for all DataObjects below that can be displayed in a Kodi List View """

    def __init__(self):
        super().__init__()
        # just a very few that all child classes have in common, so I can spare myself of using hasattr() and getattr()
        self.id: str | None = None
        self.title: str | None = None
        self.thumb: str | None = None
        self.fanart: str | None = None
        self.poster: str | None = None
        self.banner: str | None = None

    @abstractmethod
    def get_info(self, account: Account) -> Dict:
        """ return a dict with info to set on the kodi ListItem (filtered) and access some data """
        pass

    @abstractmethod
    def to_item(self, account: Account) -> Dict:
        """ Convert ourselves if needed to items"""

        pass

    @abstractmethod
    def update_playcount_from_playhead(self, playhead_data: Dict):
        pass


"""Naming convention for reference:
    Crunchyroll           XBMC
    series                collection
    season                season
    episode               episode   
"""


class SeriesData(ListableItem):
    """ A Series containing Seasons containing Episodes """

    def __init__(self, data: dict):
        super().__init__()

        panel = data.get('panel') or data
        meta = panel.get("series_metadata") or panel

        self.id = panel.get("id")
        self.title: str = panel.get("title")
        self.series_title: str = panel.get("title")
        self.series_id: str | None = panel.get("id")
        self.season_id: str | None = None
        self.plot: str = panel.get("description", "")
        self.plotoutline: str = panel.get("description", "")
        self.year: str = str(meta.get("series_launch_year")) + '-01-01'
        self.aired: str = str(meta.get("series_launch_year")) + '-01-01'
        self.premiered: str = str(meta.get("series_launch_year"))
        self.episode: int = meta.get('episode_count')
        self.season: int = meta.get('season_count')

        self.thumb: str | None = utils.get_image_from_struct(panel, "poster_tall", 2)
        self.fanart: str | None = utils.get_image_from_struct(panel, "poster_wide", 2)
        self.poster: str | None = utils.get_image_from_struct(panel, "poster_tall", 2)
        self.banner: str | None = None
        self.playcount: int = 0

    def recalc_playcount(self):
        # @todo: not sure how to get that without checking all child seasons and their episodes
        pass

    def get_info(self, account: Account) -> Dict:
        # in theory, we could also omit this method and just iterate over the objects properties and use them
        # to set data on the Kodi ListItem, but this way we are decoupled from their naming convention
        return {
            'title': self.title,
            'series_title': self.series_title,
            'season': self.season,
            'episode': self.episode,
            'plot': self.plot,
            'plotoutline': self.plotoutline,

            'playcount': self.playcount,
            'series_id': self.series_id,

            'year': self.year,
            'aired': self.aired,
            'premiered': self.premiered,

            'mediatype': 'season',

            # internally used for routing
            "mode": "seasons"
        }


class SeasonData(ListableItem):
    """ A Season/Arc of a Series containing Episodes """

    def __init__(self, data: dict):
        super().__init__()

        self.id = data.get("id")
        self.description: str = data.get("description")
        self.title: str = data.get("title")
        self.series_title: str = data.get("title")
        self.series_id: str | None = data.get("series_id")
        self.season_id: str | None = data.get("id")
        self.plot: str = data.get("description")  # does not have description. maybe object endpoint?
        self.plotoutline: str = ""
        self.year: str = ""
        self.aired: str = ""
        self.premiered: str = ""
        self.season: int = data.get('season_number')
        self.thumb: str | None = None
        self.fanart: str | None = None
        self.poster: str | None = None
        self.banner: str | None = None
        self.playcount: int = 1 if data.get('is_complete') == 'true' else 0

        self.recalc_playcount()

    def recalc_playcount(self):
        # @todo: not sure how to get that without checking all child episodes
        pass

    def get_info(self, account: Account) -> Dict:
        return {
            'title': self.title,
            'series_title': self.series_title,
            'season': self.season,
            'episode': self.episode,
            # 'plot': self.plot,
            # 'plotoutline': self.plotoutline,

            'playcount': self.playcount,
            'series_id': self.series_id,
            'season_id': self.season_id,

            # 'year': self.year,
            # 'aired': self.aired,
            # 'premiered': self.premiered,

            'mediatype': 'season',

            # internally used for routing
            "mode": "episodes"
        }


# dto
class EpisodeData(ListableItem):
    """ A single Episode of a Season of a Series """

    def __init__(self, data: dict):
        super().__init__()

        panel = data.get('panel') or data
        meta = panel.get("episode_metadata") or panel

        self.id = panel.get("id")
        self.long_title: str =  "%s #%s - %s" % (meta.get("season_title"), str( meta.get("episode_number")), panel.get("title"))
        self.episode_number: int = meta.get("episode_number")
        self.season_title: str = meta.get("season_title")
        self.title: str = meta.get("title")
        self.series_title: str = meta.get("series_title", "")
        self.duration: int = int(meta.get("duration_ms", 0) / 1000)
        self.playhead: int = data.get("playhead", 0)
        self.season: int = meta.get("season_number", 1)
        self.episode: int = meta.get("episode", 1)
        self.episode_id: str | None = panel.get("id")
        self.season_id: str | None = meta.get("season_id")
        self.series_id: str | None = meta.get("series_id")
        self.plot: str = panel.get("description", "")
        self.plotoutline: str = panel.get("description", "")
        self.year: str = meta.get("episode_air_date")[:4] if meta.get("episode_air_date") is not None else ""
        self.aired: str = meta.get("episode_air_date")[:10] if meta.get("episode_air_date") is not None else ""
        self.premiered: str = meta.get("episode_air_date")[:10] if meta.get("episode_air_date") is not None else ""
        self.thumb: str | None = utils.get_image_from_struct(panel, "thumbnail", 2)
        self.fanart: str | None = utils.get_image_from_struct(panel, "thumbnail", 2)
        self.poster: str | None = None
        self.banner: str | None = None
        self.playcount: int = 0
        self.stream_id: str | None = utils.get_stream_id_from_item(panel)

        self.recalc_playcount()

    def recalc_playcount(self):
        if self.playhead is not None and self.duration is not None:
            self.playcount = 1 if (int(self.playhead / self.duration * 100)) > 90 else 0

    def get_info(self, account: Account) -> Dict:
        # update from account
        self.playhead = self.playhead  # account.get('playhead') if account.get('playhead') is not None else self.playhead
        self.recalc_playcount()

        return {
            'title': self.title,
            'series_title': self.series_title,
            'season': self.season,
            'episode': self.episode,
            'plot': self.plot,
            'plotoutline': self.plotoutline,

            'playhead': self.playhead,
            'duration': self.duration,
            'playcount': self.playcount,

            'season_id': self.season_id,
            'series_id': self.series_id,
            'episode_id': self.episode_id,
            'stream_id': self.stream_id,

            'year': self.year,
            'aired': self.aired,
            'premiered': self.premiered,

            'mediatype': 'episode',

            # internally used for routing
            "mode": "videoplay"
        }


class CrunchyrollError(Exception):
    pass


class LoginError(Exception):
    pass
