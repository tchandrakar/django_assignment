import http.client
from .tokenutility import getActiveToken
from .models import ShipmentDetails, ShipmentItem, SyncStatus
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
    updateSellerShipmentData(getShipmentDetails(shipmentId))
    return ()


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
    return json.dumps(shipmentDetail.__dict__)
