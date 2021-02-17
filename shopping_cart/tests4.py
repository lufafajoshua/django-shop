
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid
from base64 import b64encode


token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6ImRlMmFlYTg3LWZkZDEtNDMyYS04ZDIxLTdlNDg4ZmIxZWU0OSIsImV4cGlyZXMiOiIyMDIwLTExLTI2VDE4OjM4OjI1LjMwNSIsInNlc3Npb25JZCI6IjQ1ZGQ5MTc3LWVkYmUtNGQ3Yi04YjNjLWY5ZTEyNmVjOTM4ZiJ9.dE45oVKiha78h-ZeCewSZzNfV4NoE1wJ6pKz0Fo2rFJemYzlBvEV2r3i4sRG0IHvmLeQ9OSwjVv3AFK2px5aj3nPGFu8jDYgAoIREJ6A-RhzuP0u9tYmUbKzRUtPozC3Sil-RpZcOe17xsq81Vr0mkmiRNFcPoIaN6Cx5WTyoXv4KXPJV7NR22rfnVNjm0ssm-ebeK5WFnsfk7Q1PzBFZMW5PyhbwsJyJO78lblqixIfeLQB_6BXgX09tFEhOLlI8x1a1Is3AyEKzHmTTUy4rbJ2tTFkiIokf0SRzSAhJjM-rvQDNfXTBjygGDsI4fYqTot08x3_t6wHkyjA1w4iGA"

reference_id = str(uuid.uuid4())#'de2aea87-fdd1-432a-8d21-7e488fb1ee49' 

headers = {
    # Request headers
    'Authorization': 'Bearer '+token,
    #'X-Callback-Url': 'https://winnershield.com',#Point to the transaction urls so to create the transaction information
    'X-Reference-Id': reference_id,
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
}

params = urllib.parse.urlencode({
})

body = json.dumps({
  "amount": "5000",
  "currency": "EUR",
  "externalId": "12345",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "0787579708"
  },
  "payerMessage": "Just Testing",
  "payeeNote": "Hello Successfull"
})

try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    #conn = http.client.HTTPSConnection('sandbox.momodeveloper.mtn.com')
    conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    print(response.status)
    conn.close()
except Exception as e:
    print("[Errno {0}]".format(e))
finally:
  print("Transaction in Progress")

