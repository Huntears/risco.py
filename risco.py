#!/usr/bin/env python

"""risco.py: 
Provides an easy to use interface to the RiscoCloud API
"""

import requests
import urllib3

__author__ = "Alexandre Flion (Huntears)"
__credits__ = ["Alexandre Flion (Huntears)"]

__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Alexandre Flion (Huntears)"
__email__ = "alexandre.flion@epitech.eu"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://riscocloud.com/ELAS/WebUI"
SITELOGIN_URL = BASE_URL + "/SiteLogin"
GETCPSTATE_URL = BASE_URL + "/Security/GetCPState"
GETDECTS_URL = BASE_URL +  "/Detectors/Get"

class Error(Exception):
    pass

class PasswordUsernameMismatch(Error):
    pass

class PinSiteIDMismatch(Error):
    pass

class NotAuthenticated(Error):
    pass

class Risco:
    def __init__(self):
        self.session = requests.Session()
        self.is_auth = False

    def get_cp_state(self):
        if not self.is_auth:
            raise NotAuthenticated
        return self.session.post(GETCPSTATE_URL, verify = False).json()

    def get_dects(self):
        if not self.is_auth:
            raise NotAuthenticated
        detectors = []
        res = self.session.post(GETDECTS_URL, verify = False).json()
        for i in res["detectors"]["parts"]:
            for y in i["detectors"]:
                detectors.append(y)
        return detectors

    def authenticate(self, username: str, password: str, pin: int, site_id: int) -> int:
        """Authenticate to the RiscoCloud API"""
        if ("Username/Password mismatch" in self.__auth_stage_1(username, password).text):
            raise PasswordUsernameMismatch
        if ("Incorrect PIN" in self.__auth_stage_2(pin, site_id).text):
            raise PinSiteIDMismatch
        self.is_auth = True

    def __auth_stage_1(self, username, password):
        data = {
            "username": username,
            "password": password,
            "strRedirectToEventUID": "",
            "strRedirectToSiteId": ""
        }
        return self.session.post(BASE_URL,
                                data = data,
                                verify = False)

    def __auth_stage_2(self, pin, site_id):
        data = {
            "SelectedSiteId": site_id,
            "Pin": pin
        }
        return self.session.post(SITELOGIN_URL,
                                data = data,
                                verify = False)
