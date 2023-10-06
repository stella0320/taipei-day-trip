from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import json

class TapPay(object):
    def __init__(self, url, partner_key, merchant_id, logger):
        self.__url = url
        self.__partner_key = partner_key
        self.__merchant_id = merchant_id
        self.__logger = logger
        self.__response = None
        self.__response_data = None


    def make_request(self, data=None):
        headers = {
            "Content-Type":"application/json",
            "x-api-key": self.__partner_key
        }
        
        if not data:
            return None;

        data["partner_key"] = self.__partner_key
        data["merchant_id"] = self.__merchant_id
        
        json_data = json.dumps(data).encode("utf-8")
        request = Request(self.__url, data=json_data, headers=headers)
        
        try:
            with urlopen(request, timeout=10) as response:
                self.__response = response
                self.__response_data = self.handleJsonResponse()
                self.__logger.info('status:%s, response:%s' % (response.status, self.__response_data))
                
            return self.__response
        except HTTPError as error:
            self.__logger.error('status:%s, error_info:%s' % (error.status, error.info))
        except URLError as error:
            print(error.info)
        except TimeoutError as error:
            print("time out")

    def handleJsonResponse(self):
        response = self.__response
        if response:
            encoding = response.info().get_content_charset('utf-8')
            data = response.read()
            json_data = json.loads(data.decode(encoding))
            return json_data

    def getJsonResponse(self):
        return self.__response_data