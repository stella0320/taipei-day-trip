from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import json

def make_request(url, headers=None, data=None):
    request = Request(url, data=data, headers=headers)
    try:
        with urlopen(request, timeout=1000) as response:
            print(response.status)
            print(response)
            return response.read(), response
    except HTTPError as error:
        print(error.status, error.info)
    except URLError as error:
        print(error.info)
    except TimeoutError as error:
        print("time out")
    

url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
app_key = 'app_voc7R7iqSLwz6G317QB4Bl2QaYq6eFd3aRABDMMqoicm3nijQDX8JuxW5AES'
partner_key = 'partner_yvNAtvcEOFaJG9IimrMvG5FxsPFBbtmBKxta3SNRnm2yxgaTWJ0USEMG'
merchant_id = 'jessie0320_NCCC'
data = {
  "prime": '9b60023e6c2328463253857e8a29bc9440d278d7c621a7a51ada66b0b7361418',
  "partner_key": partner_key,
  "merchant_id": merchant_id,
  "details":"Order id:" + 1,
  "amount": 100,
  "bank_transaction_id": "20231004145701",
  "cardholder": {
      "phone_number": "+886923456789",
      "name": "王小明",
      "email": "LittleMing@Wang.com"
  }
}
headers = {
    "Content-Type":"application/json",
    "x-api-key": partner_key
}
json_data = json.dumps(data).encode("utf-8")
print(json_data)
body, response = make_request(url, data=json_data, headers=headers)
print(body)