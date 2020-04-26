from celery import shared_task
import time
from .shipments import getAndSaveShipmentDetails

@shared_task
def sync_shipment_details(shipmentId):
    time.sleep(5)
    return getAndSaveShipmentDetails(shipmentId)