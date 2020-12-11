from utils.address import AddressField
from django.db import models


class Order(models.Model):
    """
    Order Model for the Seller
    """

    class Status(models.TextChoices):
        PLACED = "Pl", "Placed"
        PROCESSED = "Pr", "Processed"
        PACKED = "Pk", "Packed"
        SHIPPED = "Sh", "Shipped"
        DELIVERED = "Dl", "Delivered"
        REJECTED = "Rj", "Rejected"
        RETURNED = "Rt", "Returned"
        RECEIVED = "Rc", "Received"  # Received Back

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(
        "products.Product", on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    placed_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, default=Status.PLACED, max_length=2)
    address = AddressField()

    @property
    def seller(self):
        return self.product.seller
