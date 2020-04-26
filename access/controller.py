
from django.http import HttpResponse
from .tokenutility import *
from .jsonconversions import *
from .dtos import SellerTokenDTO
from .shipments import getShipmentDetailFromDB
from .syncshipments import syncAllShipments

def getToken(request):
    return HttpResponse(getActiveToken(), content_type='application/json')

def test(request):
    print("getLatestToken")
    #jsonResponse = serialize('json', getLatestToken(), cls=LazyEncoder)
    latestToken = getActiveToken()
    sellerTokenDTO = SellerTokenDTO(latestToken.access_token, latestToken.expiry_time.strftime("%m/%d/%Y, %H:%M:%S"))
    return HttpResponse(SellerTokenEncoder().encode(sellerTokenDTO), content_type='application/json')


def startSync(request):
    syncStatus = syncAllShipments()
    response = "Triggered sync. Status = "+syncStatus
    return HttpResponse(response)

def getShipmentDetail(request, shipmentId):
    getShipmentDetailFromDB(shipmentId)