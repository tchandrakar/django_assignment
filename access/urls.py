from django.urls import path
from . import controller, views

urlpatterns = [
    path('get/', controller.getToken, name='bolo-token'),
    path('latest/', controller.test, name='test-token'),
    path('startsync/', controller.startSync, name='start-sync'),
    path('shipments/<int:shipmentId>', controller.getShipmentDetail, name='shipment-detail'),
    #path('shipmentDetails', controller.shipmentDetails, name='shipment-details')

]
