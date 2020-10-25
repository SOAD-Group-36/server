from django.db import models


class Product(models.Model):
    seller = models.ForeignKey("sellers.Seller", on_delete=models.CASCADE)
    name = models.CharField(max_length=180)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    weight = models.IntegerField("Weight(gm)")
    length = models.IntegerField("Length(mm)")
    height = models.IntegerField("Height(mm)")
    width = models.IntegerField("Width(mm)")
    images = models.ManyToManyField("products.ProductImage")


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product/images")

    @property
    def url(self):
        return self.image.url
