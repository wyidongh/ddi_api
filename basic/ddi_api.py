import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth


class ddi_api(object):


    def get(self,url,params=None,auth=None):
        self.api_error = None
        try:
            r = requests.get(url=url,params=params,timeout=2,verify=False,auth=auth)
        except BaseException as msg:
            self.api_error = str(msg)
        else:
            try:
                status_code = r.status_code
                res = r.json()
                print(res)
                return status_code, res
            except ValueError:
                self.api_error = "No JSON object could be decoded"



    def post(self,url,json=None,auth=None):
        self.api_error = None
        try:
            r = requests.post(url=url,json=json,timeout=2,verify=False,auth=auth)
        except BaseException as msg:
            self.api_error = str(msg)
        else:
            try:
                status_code = r.status_code
                res = r.json()
                print(res)
                return status_code, res
            except ValueError:
                self.api_error = "No JSON object could be decoded"

    def put(self,url,json=None,auth=None):
        self.api_error = None
        try:
            r = requests.put(url=url,json=json,timeout=2,verify=False,auth=auth)
        except BaseException as msg:
            self.api_error = str(msg)
        else:
            try:
                status_code = r.status_code
                res = r.json()
                print(res)
                return status_code, res
            except ValueError:
                self.api_error = "No JSON object could be decoded"

    def delete(self,url,params=None,auth=None):
        self.api_error = None
        try:
            r = requests.delete(url=url,params=params,timeout=2,verify=False,auth=auth)
        except BaseException as msg:
            self.api_error = str(msg)
        else:
            try:
                status_code = r.status_code
                res = r.json()
                print(res)
                return status_code, res
            except ValueError:
                self.api_error = "No JSON object could be decoded"


