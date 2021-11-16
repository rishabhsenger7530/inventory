from django.contrib import admin
from .models import UserProfile, Product, Sales,OrderProduct,Followupnotes
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Sales)
admin.site.register(OrderProduct)
admin.site.register(Followupnotes)