from django.db import models

# Create your models here.

class Product(models.Model):
    productId = models.AutoField
    productName = models.CharField(max_length = 50,default = "")
    category = models.CharField(max_length = 50,default = "")
    sub_category = models.CharField(max_length = 50,default = "")
    price = models.IntegerField(default = 0)
    desc = models.CharField(max_length = 300)
    pubDate = models.DateField()
    image = models.ImageField(upload_to = "shop/images", default = "")

    def __str__ (self):
        return self.productName
    
class Contact(models.Model):
    msgId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50,default = '')
    userEmail = models.CharField(max_length=50,default='')
    userPhone = models.CharField(max_length=15,default='')
    userMessage = models.CharField(max_length=500,default='')
    messageDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.userName
    
class Order(models.Model):
    ordId = models.AutoField(primary_key = True)
    cart = models.CharField(max_length = 2000)
    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 15,default='')
    address = models.CharField(max_length = 300)
    city = models.CharField(max_length = 30)
    state = models.CharField(max_length = 30)
    zipCode = models.CharField(max_length = 10)

    def __str__(self):
        return self.name
