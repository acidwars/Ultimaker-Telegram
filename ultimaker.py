#!/usr/bin/env python3

import requests
import json
import os
import time
from pprint import pprint

class Ultimaker3:

    def __init__(self, ip, application):
        self.__ip = ip
        self.__application = application
        self.__session = requests.sessions.Session()
        self.__setAuthData("", "")

    def __setAuthData(self, id, key):
        self.__auth_id = id
        self.__auth_key = key
        self.__auth = requests.auth.HTTPDigestAuth(
            self.__auth_id, self.__auth_key)

    def loadAuth(self, filename):
        try:
            data = json.load(open(filename, "rt"))
            self.__setAuthData(data["id"], data["key"])
        except IOError:
            self.__checkAuth()
            self.saveAuth(filename)
        if not self.__checkAuth():
            self.saveAuth(filename)

    # Save the authentication data to a file.
    def saveAuth(self, filename):
        json.dump({"id": self.__auth_id, "key": self.__auth_key},
                  open(filename, "wt"))

  
    def __checkAuth(self):
        if self.__auth_id == "" or self.get("api/v1/auth/verify").status_code != 200:
            print("Auth check failed, requesting new authentication")
            response = self.post(
                "api/v1/auth/request", data={"application": self.__application,
                    "user": "henrik"})
            if response.status_code != 200:
                raise RuntimeError("Failed to request new API key")
            data = response.json()
            self.__setAuthData(data["id"], data["key"])
            while True:
                time.sleep(1)
                response = self.get("api/v1/auth/check/%s" % (self.__auth_id))
                data = response.json()
                print(data["message"])
                if data["message"] == "unknown" or "authorized":
                    print("Authorized.")
                    break
                if data["message"] == "unauthorized":
                    raise RuntimeError("Authorization denied")
            return False
        else:
             pprint("true")
        return True

    # Do a new HTTP request to the printer. It formats data as JSON, and fills in the IP part of the URL.
    def request(self, method, path, **kwargs):
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
            if "headers" not in kwargs:
                kwargs["headers"] = {"Content-type": "application/json"}
        return self.__session.request(method, "http://%s/%s" % (self.__ip, path), auth=self.__auth, **kwargs)

    # Shorthand function to do a "GET" request.
    def get(self, path, **kwargs):
        return self.request("get", path, **kwargs)

    # Shorthand function to do a "PUT" request.
    def put(self, path, **kwargs):
        return self.request("put", path, **kwargs)

    # Shorthand function to do a "POST" request.
    def post(self, path, **kwargs):
        return self.request("post", path, **kwargs)


