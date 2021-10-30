from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime
# from datetime import date
CHOICES = (
        ('A', 'Admin'),
        ('S', 'Sales'),
        ('C', 'Collection'),
    )
class User(User):
    usertype    = models.CharField(max_length=1,choices=CHOICES)
    contact     = models.BigIntegerField()
    sales_code  = models.CharField(max_length=6,default="123454")


class Sales(models.Model):
    b_firmname    = models.CharField(max_length=250, blank=True)
    b_addr1       = models.CharField(max_length=250, blank=True)
    b_addr2       = models.CharField(max_length=250, blank=True)
    b_city        = models.CharField(max_length=250, blank=True)
    b_state       = models.CharField(max_length=250, blank=True)
    b_zip         = models.CharField(max_length=250, blank=True)
    b_country     = models.CharField(max_length=250, blank=True)
    s_firmname    = models.CharField(max_length=250, blank=True)
    s_addr1       = models.CharField(max_length=250, blank=True)
    s_addr2       = models.CharField(max_length=250, blank=True)
    s_city        = models.CharField(max_length=250, blank=True)
    s_state       = models.CharField(max_length=250, blank=True)
    s_zip         = models.CharField(max_length=250, blank=True)
    s_country     = models.CharField(max_length=250, blank=True)
    b_date        = models.DateField()
    b_buyer       = models.CharField(max_length=250, blank=True)
    b_purchase_order= models.CharField(max_length=250, blank=True)
    b_tirms       = models.CharField(max_length=250, blank=True)
    contact1      = models.CharField(max_length=250, blank=True)
    contact2      = models.CharField(max_length=250, blank=True)
    email         = models.CharField(max_length=250, blank=True)
    payment_due_date = models.DateField(null=True)
    #created_by    = models.ForeignKey(User,default="b@gmail.com", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.payment_due_date is None:
            self.payment_due_date =datetime.datetime.now()+datetime.timedelta(days=30)
        super(Sales, self).save(*args, **kwargs)
    


class Product(models.Model):
    item              = models.CharField(max_length=250)
    production_desc   = models.CharField(max_length=250)
    unitprice         = models.CharField(max_length=250)
    

class OrderProduct(models.Model):
    sale              = models.ForeignKey(Sales,default="1",on_delete=models.CASCADE)
    quantity          = models.IntegerField()
    item              = models.ForeignKey(Product,default="1",on_delete=models.CASCADE)
    ou                = models.CharField(max_length=250)
    production_desc   = models.CharField(max_length=250)
    unitprice         = models.CharField(max_length=250)
    extend            = models.CharField(max_length=250)




class Followupnotes(models.Model):
    sale              = models.ForeignKey(Sales,default="b@gmail.com",on_delete=models.CASCADE)
    content           = models.TextField()
    date              = models.DateField()

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        return super(Followupnotes, self).save(*args, **kwargs)


