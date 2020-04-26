import http.client
from .tokenutility import getActiveToken
from .models import SyncStatus
import json
from datetime import datetime
from .tasks import sync_shipment_details


def getSellerShipments(page, fulfilment_method):
    page = str(page)
    requestUrl = "api.bol.com"
    conn = http.client.HTTPSConnection(requestUrl)
    payload = ''
    token = getActiveToken().access_token
    authHeader = 'Bearer ' + token
    headers = {
        'Accept': 'application/vnd.retailer.v3+json',
        'Authorization': authHeader
    }
    queryParams = '?page='+page+'&fulfilment-method='+fulfilment_method
    path = "/retailer/shipments" + queryParams
    print(path)
    conn.request("GET", path, payload, headers)
    res = conn.getresponse()
    jsonData = json.loads(res.read().decode("utf-8"))
    print(jsonData)
    if(jsonData != None):
        return jsonData['shipments']
    else:
        return ()

def syncAllShipments():
    def getAllShipmentPages(page, type):
        paginatedShipments = getSellerShipments(page, type)
        while (paginatedShipments != None):
            # Sync to RabbitMq
            for i in paginatedShipments:
                shipmentid = i['shipmentId']
                print(shipmentid)
                sync_shipment_details(shipmentid)

            page += 1
            paginatedShipments = getSellerShipments(page, type)


    def updateSyncStatus():
        latestSyncStatus = SyncStatus.objects.latest()
        latestSyncStatus.sync_in_progress = False
        latestSyncStatus.sync_end_time = datetime.now
        latestSyncStatus.save()

    def addNewSyncStatus():
        now = datetime.now
        SyncStatus(sync_in_progress=True, sync_start_time=now, sync_end_time=None)

    syncStatus = SyncStatus.objects
    if(syncStatus.exists() and syncStatus.latest("id").sync_in_progress):
        return "Sync is in progress"


    addNewSyncStatus()
    getAllShipmentPages(1, "FBR")
    getAllShipmentPages(1, "FBB")
    updateSyncStatus()
    return "Sync Done"
