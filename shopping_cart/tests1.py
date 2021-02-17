
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid
from base64 import b64encode

"""
PAyments with Mtn Momo API
"""

api_user = 'de2aea87-fdd1-432a-8d21-7e488fb1ee49'
api_key = '002c242c2aa047b7926c3d86dbf1b9a5' 
api_user_and_key  = api_user+':'+api_key
#api_user_and_key  = api_user + api_key
#api_user_and_key_bytes = api_user_and_key.encode('ascii')
api_user_and_key_bytes = base64.b64encode(api_user_and_key.encode()).decode()

#encoded = base64.b64encode(api_user_and_key_bytes)

#reference_id = str(uuid.uuid4())
headers = {
    # Request headers
    'Authorization': "Basic "+api_user_and_key_bytes,
    #'Authorization': 'Basic' +api_user_and_key_bytes,
    
        # 'X-Callback-Url': '',
        # 'X-Reference-Id': '6cb5711b-5d29-4053-aaa1-516ec394f044',
    #'X-Target-Environment': 'oauth2',
    #'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
}

params = urllib.parse.urlencode({
})

    # body = json.dumps({
    # "providerCallbackHost": "https://winnershield.com" })

try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')#replace with ericssonbasicapi2.azure-api.net when having a new connection
    conn.request("POST", "/collection/token/?%s" % params, "{body}", headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}]".format(e))  
    


    # try:
    #     conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    #     conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, "{body}", headers)
    #     response = conn.getresponse()
    #         # print(response.status)
    #         # print(response.reason)
    #     data = response.read()
    #     print(data)
    #     conn.close()
    # except Exception as e:
    #     print("[Errno {0}]".format(e))  

#Access Token
#b'{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6ImRlMmFlYTg3LWZkZDEtNDMyYS04ZDIxLTdlNDg4ZmIxZWU0OSIsImV4cGlyZXMiOiIyMDIwLTExLTE1VDExOjMzOjExLjE1MSIsInNlc3Npb25JZCI6IjU0YzYwZWQzLTdiZjItNDg5Ny04NWU0LTA1MjFiNjFlYTJlOSJ9.lfEl-g55jmU2GEepnIBIAnUL79eI3wlFpaQd4E_QrU6F3FFNz-csgEPMDnGF0ynEmFgeWkXrUUeROmNlj32YtN5C32DmfuPG3zwfvcleGv-WonVcnITtlBN1B5tbv8QVX1n9k9soCS17R4de0lL3nXUtjQQM6ndnO7eqFYBihjMGBLbxEIPUhLEHq-N9Y4tuB1huQ3Bk8li1hAIR-FlwLBe-X4hxeKD8t1dRHoC4jqEOi7JISXBxcZpt4f-CosxQK-c5ndVUp1FpHP7U5nfieSFa7I8gEvEjTWq3lYAJQZKF3zKWrCB9a7rESoI896b1pJbzz-okV0LQGhaFg7ONkQ","token_type":"access_token","expires_in":3600}'    