from django.db import models

class SellerToken(models.Model):
    access_token = models.TextField()
    expiry_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)

class SyncStatus(models.Model):
    id = models.AutoField(primary_key=True)
    sync_in_progress = models.BooleanField()
    sync_start_time = models.DateTimeField()
    sync_end_time = models.DateTimeField()

class ShipmentDetails(models.Model):
    shipment_id = models.BigIntegerField(primary_key=True)
    pick_up_point = models.BooleanField()
    shipment_date = models.DateTimeField()
    shipment_reference = models.BigIntegerField(default=None)
    transport_id = models.BigIntegerField()
    transporter_code = models.TextField()
    track_and_trace = models.TextField()
    salutation_code = models.BigIntegerField()
    zip_code = models.TextField()
    country_code = models.TextField()
    email = models.TextField(default=None)


class ShipmentItem(models.Model):
    shipment_id = models.ForeignKey(ShipmentDetails, to_field='shipment_id', on_delete=models.CASCADE)
    order_item_id = models.BigIntegerField()
    order_id = models.BigIntegerField()
    order_date = models.DateTimeField()
    latest_delivery_date = models.DateTimeField()
    ean = models.BigIntegerField()
    title = models.TextField()
    quantity = models.BigIntegerField()
    offer_price = models.BigIntegerField()
    offer_condition = models.TextField()
    offer_reference = models.TextField()
    fulfillment_method = models.TextField()

