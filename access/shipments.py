import http.client

from asgiref.sync import sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tokenutility import getActiveToken
from .models import ShipmentDetails, ShipmentItem, SyncStatus, ShipmentIdSyncStatus
import json


def updateSellerShipmentData(jsonData):
    jsonData = dict(jsonData)
    shipmentId = jsonData["shipmentId"]
    existingshipmentDetails = ShipmentDetails.objects.filter(shipment_id=shipmentId)
    if (existingshipmentDetails.exists()):
        existingshipmentDetails.first().delete()
    transport = dict(jsonData["transport"])
    customerDetails = dict(jsonData["customerDetails"])
    email = ""
    shipment_reference = -1
    if (customerDetails.__contains__("email")):
        email = customerDetails["email"]

    if (jsonData.__contains__("shipmentReference")):
        shipment_reference = jsonData["shipmentReference"]

    shipmentSummary = ShipmentDetails(shipment_id=shipmentId, pick_up_point=jsonData["pickUpPoint"],
                                      shipment_date=jsonData["shipmentDate"], shipment_reference=shipment_reference,
                                      transport_id=transport["transportId"],
                                      transporter_code=transport["transporterCode"],
                                      track_and_trace=transport["trackAndTrace"],
                                      salutation_code=customerDetails["salutationCode"],
                                      zip_code=customerDetails["zipCode"], country_code=customerDetails["countryCode"],
                                      email=email)
    ShipmentDetails.save(shipmentSummary)
    for j in jsonData["shipmentItems"]:
        j = dict(j)
        offer_reference = ""
        if j.__contains__("offerReference"):
            offer_reference = j["offerReference"]

        shipmentItem = ShipmentItem(shipment_id=shipmentSummary, order_item_id=j["orderItemId"], order_id=j["orderId"],
                                    order_date=j["orderDate"], latest_delivery_date=j["latestDeliveryDate"],
                                    ean=j["ean"], title=j["title"], quantity=j["quantity"], offer_price=j["offerPrice"],
                                    offer_condition=j["offerCondition"], offer_reference=offer_reference,
                                    fulfillment_method=j["fulfilmentMethod"])
        shipmentItem.save()

    return ()

def getAndSaveShipmentDetails(shipmentId):
    shipmentIds = ShipmentIdSyncStatus.objects
    if shipmentIds.exists():
        shipmentIds.filter(shipment_id=shipmentId).delete()
    ShipmentIdSyncStatus(shipment_id=shipmentId, sync_in_progress=1).save()
    # updateSellerShipmentData(getShipmentDetails(shipmentId))
    return '{} Shipment Synced!'.format(shipmentId)

@receiver(post_save, sender=ShipmentIdSyncStatus)
def addInShipmentDetails(sender, **kwargs):
    for i in ShipmentIdSyncStatus.objects.all():
        if i.sync_in_progress:
            updateSellerShipmentData(getShipmentDetails(i.shipment_id))
            i.sync_in_progress = False
            i.save()

def getShipmentDetails(shipmentId):
    conn = http.client.HTTPSConnection("api.bol.com")
    payload = ''
    token = getActiveToken().access_token
    authHeader = 'Bearer ' + token
    headers = {
        'Accept': 'application/vnd.retailer.v3+json',
        'Authorization': authHeader
    }
    conn.request("GET", "/retailer/shipments/" + str(shipmentId), payload, headers)
    res = conn.getresponse()
    jsonData = json.loads(res.read().decode("utf-8"))
    print(jsonData)
    return jsonData


def getShipmentDetailFromDB(shipmentId):
    shipmentDetail = ShipmentDetails.object.filter(shipmentId=shipmentId).first()
    shipmentItems = ShipmentItem.objects.filter(shipmentId=shipmentId)
    return json.dumps(dict(shipmentDetail).add("shipmentItems", shipmentItems))
