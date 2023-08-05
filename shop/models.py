from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    SubCategory = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=5000)
    price = models.IntegerField(default=0)
    publish_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name



class contact(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=15, default="")
    query = models.TextField(default='')

    def __str__(self):
        return f'Query by {self.name}'



class order(models.Model):
    placed_order_id = models.AutoField(primary_key=True)
    order_ids = models.CharField(max_length=5000)
    cost = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    Address01 = models.CharField(max_length=500, default="")
    Address02= models.CharField(max_length=500, default='')
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=15, default="")
    pin_code = models.CharField(max_length=10, default='')

    def __str__(self):
        return f'order by {self.name}'




class tracker(models.Model):
    tracker_id = models.IntegerField(default=0)
    timeStamp = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=5000, default='')

    def __str__(self):
        return f'Updated status for Order ID: {self.tracker_id}...'



