
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid


headers = {
    # Request headers
    #'X-Reference-Id': 'de2aea87-fdd1-432a-8d21-7e488fb1ee49',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
}


params = urllib.parse.urlencode({
})

body = json.dumps({
  "providerCallbackHost": "https://winnershield.com" })
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", "/v1_0/apiuser/de2aea87-fdd1-432a-8d21-7e488fb1ee49/apikey?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] ".format(e))

