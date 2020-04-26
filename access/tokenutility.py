from asgiref.sync import sync_to_async

from .models import SellerToken
from datetime import datetime
import http.client
import json
import datetime
from datetime import timedelta,timezone

def generateNewToken():
    conn = http.client.HTTPSConnection("login.bol.com")
    payload = ''
    headers = {
        'Authorization': 'Basic NjliZDgzZjEtMTE3Mi00YjAyLTgyMWEtYjVhMmFmNWEzMmRhOk5mYWluQ2NtYmFmaUNVaXV0VjdJS21qbjhOYk9DYnc2WGMxNmEtX01EVnlDMGpoZmJla05JcFEzejNzTlVIaE5KSkVoSzNPUlNiaDhXV2JmOXpTR3BR'
    }
    conn.request("POST", "/token?grant_type=client_credentials", payload, headers)
    res = conn.getresponse()
    data = res.read()
    jsonData = json.loads(data.decode("utf-8"))
    return jsonData["access_token"]

def updateToken(accessToken):
    creationTime = datetime.datetime.now(tz=timezone.utc)
    expiryTime = creationTime + timedelta(seconds=250)
    newToken = SellerToken(access_token = accessToken, expiry_time = expiryTime, created_on = creationTime)
    SellerToken.objects.all().delete()
    newToken.save()
    return ()

def getLatestToken():
    tokens = SellerToken.objects
    if tokens.exists():
        return tokens.first()
    else:
        updateToken(generateNewToken())
        return getLatestToken()

def getActiveToken():
    latestToken = getLatestToken()
    if latestToken.expiry_time <= datetime.datetime.now(tz=timezone.utc):
        updateToken(generateNewToken())
        latestToken = getLatestToken()
    return latestToken


