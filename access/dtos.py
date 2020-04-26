class SellerTokenDTO:
    def __init__(self, token, expiry_time):
        self.token = token
        self.expiry_time = expiry_time

class ShipmentItemDTO:
    def __init__(self, orderItemId, orderId):
        self.orderItemId = orderItemId
        self.orderId = orderId

class TransportDTO:
    def __init__(self, transportId):
        self.transportId = transportId

class ShipmentSummaryDTO:
    def __init__(self, shipmentId, shipmentDate, shipmentItems, transport):
        self.shipmentId = shipmentId
        self.shipmentDate = shipmentDate
        self.shipmentItems = shipmentItems
        self.transport = transport
