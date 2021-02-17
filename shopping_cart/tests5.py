
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, uuid
from base64 import b64encode

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSMjU2In0.eyJjbGllbnRJZCI6ImRlMmFlYTg3LWZkZDEtNDMyYS04ZDIxLTdlNDg4ZmIxZWU0OSIsImV4cGlyZXMiOiIyMDIwLTExLTMwVDE5OjIyOjE0LjExOSIsInNlc3Npb25JZCI6ImMzYjk4ZGNjLTAyYTgtNDY4MS04YmRkLTM2NzdjYjQyYjIwYyJ9.XT7k6aRVSef_QMUfML5QtDbtWSTQCs1U8hrIkDYOwPUy2rzwSk3VAOuI67MEU8zsf9ZUIblle61nv3msE-a0m4t06SpLe9WJkx5Mh_0LI5UPwPNhNzLGKax69U5XDcLbYAvzzofKCHLk2nb3P0MWZpNo01FFlTs6i-ModA802S1Bw6ja3IwRrfNIzd6fOVlJrmPGOsHVj4K_r8BINm9_6cNQY_gTwcVibVg_e05s4DKq8X4BB3r1DwOFncEHNQ4-dnX5M3crJXzWjeKrlBLWXcgqgTodOi6JnsbPXbqSvB9S40d4CDL81jr_KXrnL16IAwvuTMRaVh8N9vmr2c6CDA"
reference_id = str(uuid.uuid4())
headers = {
    # Request headersi
    'Authorization': 'Bearer '+token,
    #'X-Callback-Url': <replace with own http://myapp.com/momoapi/callback>,
    'X-Reference-Id': reference_id,
    'X-Target-Environment': 'sandbox',
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'bda4d094a1d840d4a709a4a4359b9b02',
}

params = urllib.parse.urlencode({
})

body = json.dumps({
  "amount": "5000",
  "currency": "EUR",#use UGX in production
  "externalId": "12345",
  "payer": {
    "partyIdType": "MSISDN",
    "partyId": "0787579708"
  },
  "payerMessage": "test message",
  "payeeNote": "test note"
})
try:
    conn = http.client.HTTPSConnection('ericssonbasicapi2.azure-api.net')
    conn.request("POST", "/collection/v1_0/requesttopay?%s" % params, body, headers)
    response = conn.getresponse()
    print(response.status)
    print(response.reason)
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] ".format(e))