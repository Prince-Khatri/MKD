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