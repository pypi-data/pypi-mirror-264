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

import random, sys, logging, argparse

import utils

from account import Account
from api import API

def main(argv):
    """Main function for the settings
    """
    account = Account(argv)

    # get account information
    if argv.username is not None and argv.username != "":
        account.settings.crunchyroll_username = argv.username

    if hasattr(account.settings, "crunchyroll_username"):
        username = account.settings.crunchyroll_username
    else:
        utils.crunchy_log(account, "No crunchyroll username", logging.ERROR)
        exit(11)

    if argv.password is not None and argv.password != "":
        account.settings.crunchyroll_password = argv.password
    
    if hasattr(account.settings, "crunchyroll_password"):
        password = account.settings.crunchyroll_password
    else:
        utils.crunchy_log(account, "No crunchyroll password", logging.ERROR)
        exit(12)

    if argv.subtitle is not None and argv.subtitle != "":
        account.settings.subtitle = argv.subtitle
    
    if hasattr(account.settings, "subtitle"):
        account.subtitle = account.settings.subtitle
    else:
        utils.crunchy_log(account, "subtitle", logging.ERROR)
        exit(13)

    if argv.subtitle_fallback is not None and argv.subtitle_fallback != "":
        account.settings.subtitle_fallback = argv.subtitle_fallback
    
    if hasattr(account.settings, "subtitle_fallback"):
        account.subtitle_fallback = account.settings.subtitle_fallback
    else:
        utils.crunchy_log(account, "subtitle_fallback", logging.ERROR)
        exit(13)

    if hasattr(account.settings, "device_id"):
        account.device_id = account.settings.device_id

        # get account information
    if argv.profile_path is not None and argv.profile_path != "":
        account.settings.profile_path = argv.profile_path

    account.profile_path = account.settings.profile_path

    if not account.device_id:
        char_set = "0123456789abcdefghijklmnopqrstuvwxyz0123456789"
        account.device_id = (
                "".join(random.sample(char_set, 8)) +
                "-" +
                "".join(account.settings.name[0:4]) +
                "-" +
                "".join(random.sample(char_set, 4)) +
                "-" +
                "".join(random.sample(char_set, 4)) +
                "-" +
                "".join(random.sample(char_set, 12))
        )
        account.settings.device_id = account.device_id
    
    account.settings.save()


    api = API(account=account)

    if not (username and password):
        # open settings settings
        utils.crunchy_log(account, "Login successful", logging.INFO)
        return False
    else:
        # login
        if api.start():
            utils.crunchy_log(account, "Login successful", logging.INFO)

            _list = check_arg(account, api, argv)
            if _list is None:
                utils.crunchy_log(account, "search mode '" + argv.mode + "' failed", logging.ERROR)
                return None
            text = ""
            if argv.field:
                field = list(argv.field.split(","))
            else:
                field = list()
            for item in _list:
                text+="\n"
                if type(item) is str:
                    text+=item 
                else:
                    for key in item.__dict__:
                        if field.__len__():
                            for f in field:
                                if f == key:
                                    text += key + "=>" + str(item.__dict__[key]) + "\t"
                        else:
                            if item.__dict__[key] is not None and item.__dict__[key] != "" :
                                text += key + "=>" + str(item.__dict__[key]) + "\t"
        else:
            # login failed
            utils.crunchy_log(account, "Login failed", logging.ERROR)
            return False


def check_arg(account, api: API, argv):
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
        filter_categories = api.list_categories(account)
        if argv.category_filter in filter_categories:
            return api.search_items_by_category(account)
        else:
            utils.crunchy_log(account, "list category filter %s" % str(filter_categories), logging.INFO)
            return filter_categories

    if argv.season_filter is not None:
        season_categories = api.list_seasons(account)
        if argv.season_filter not in season_categories:
            utils.crunchy_log(account, "list category filter %s" % str(season_categories), logging.INFO)
            return season_categories
        else:
            return api.search_items_by_season(account)

    if argv.id is not None and argv.search_type == 'series':
        return api.search_season_by_series_id(account)

    if argv.search is not None:
        return api.search_items_by_string(account)

    if argv.crunchylist_filter is not None:
        filter_crunchylists = api.list_crunchylists(account)
        if argv.crunchylist_filter in filter_crunchylists:
            return api.search_items_by_crunchylist(account)
        else:
            utils.crunchy_log(account, "list crunchylist filter %s" % str(filter_crunchylists), logging.INFO)
            return filter_crunchylists

    if argv.playlist:
        return api.get_playlist(account)

    utils.crunchy_log(account, "mode '%s' does not exist" % str(api.mode), logging.ERROR)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--field","-f", type=str, help="show only field", required=False)
    groupAPI = parser.add_argument_group('API')
    groupAPI.add_argument("--season_id", type=str, required=False)
    groupAPI.add_argument("--search","-s", type=str, help="string search", required=False)
    groupAPI.add_argument("--search_type", type=str, help="search type", required=False, default="series")
    groupAPI.add_argument("--id", type=str, required=False)
    groupAPI.add_argument("--crunchylist_filter", help="list filter or filter by crunchylist", required=False, action='store', const="", nargs='?', type = str)
    groupAPI.add_argument("--category_filter", help="list filter or filter by category", required=False, action='store', const="", nargs='?', type = str)
    groupAPI.add_argument("--season_filter", help="list filter or filter by saison", required=False, action='store', const="", nargs='?', type = str)
    groupAPI.add_argument("--playlist", help="playlist", required=False, action='store_true')

    groupLogin = parser.add_argument_group('Authentication with login password',"")
    groupLogin.add_argument("-u", "--username", type=str, help="username", required=False)
    groupLogin.add_argument("-p", "--password", type=str, help="password", required=False)
    groupLogin.add_argument("--profile_path", type=str, help="profile_path", required=False, default="./")
    groupLogin.add_argument("--setting_file", type=str, help="setting_file", required=False, default="settings.json")
    groupLogin.add_argument("--subtitle", type=str, help="""
    en-US, en-GB , es-419, es-ES, pt-BR, pt-PT, fr-FR, de-DE, ar-ME, it-IT, ru-RU, en-US
    """, required=False)
    groupLogin.add_argument("--subtitle-fallback", type=str, help="""
    en-US, en-GB , es-419, es-ES, pt-BR, pt-PT, fr-FR, de-DE, ar-ME, it-IT, ru-RU, en-US
    """, required=False)

    argv = parser.parse_args()

    main(argv)