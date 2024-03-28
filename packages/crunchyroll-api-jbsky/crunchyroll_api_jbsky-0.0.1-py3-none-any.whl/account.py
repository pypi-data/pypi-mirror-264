# MIT License
# 
# Crunchyroll API 
# Use the crunchyroll API with an authenticated premium account
# Copyright (C) 2024 jbsky
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json, os

class Setting:
        def __init__(self, setting_file = "./settings.json", profile_path = "./"):
            self.setting_file = setting_file
            self.profile_path = profile_path

            if os.path.isfile(self.setting_file):
                with open(self.setting_file, "r") as infile:
                    setting = json.load(infile)
            
                for k, v in setting.items():
                    self.__setattr__(k, v)

        def setprofile(self, profile_path):
            self.__setattr__("profile_path", profile_path)

        def save(self):
                with open(self.setting_file, "w") as outfile:
                     outfile.write(json.dumps(self.__dict__, indent=2))
        
        @property
        def name(self):
              return "generic"


class Account(object):
    """Arguments class
    Hold all arguments passed to the script and also persistent user data and
    reference to the addon. It is intended to hold all data necessary for the
    script.
    """

    def __init__(self, argv):
        """Initialize arguments object
        Hold also references to the addon which can't be kept at module level.
        """
        # addon specific data

        self.settings = Setting(argv.setting_file)
        self.cj = None
        self.device_id = None
        self.session_restart = False

        for i in argv.__dict__:
            if argv.__dict__[i] is not None:
                self.__setattr__(i, argv.__dict__[i])
        
