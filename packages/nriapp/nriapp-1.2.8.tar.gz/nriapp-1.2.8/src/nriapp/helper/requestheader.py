import json
import requests, json, pickle, ast
from urllib.parse import parse_qs
import os
import email
from io import StringIO
import sys
sys.path.append("..") # Adds higher directory to python modules path.

#from helper.pylog import *

#from PyLog import *

class RequestHeader:
    def __init__(self, driver, rqst_url):
        self.drv = driver
        self.rqst_url = rqst_url
        self.body = {}
        self.status_code = 0
        self.headers = ""

        for rqst in driver.requests:
            counter=0
            if rqst_url in rqst.url:
                counter+=1
                self.status_code = rqst.response.status_code
                self.body = rqst.body.decode('utf-8')  
                self.headers = rqst.headers
                self.response_header = rqst.response.headers._headers
                self.params = rqst.params
                #print( rqst.url, 
                #    rqst.response.status_code,
                #    rqst.headers.__str__()
                #    )
                if counter >=1:
                    break

    def get_param(self, param):                 #dictionary output

            _, raw_headers = self.headers.__str__().split("\n", 1)
            msg = email.message_from_file(StringIO(raw_headers))
            c = [a for a in msg.items() if param in a][0][1]
            return {b[0]: b[1] for b in [a.split("=") for a in c.split("; ")]}
