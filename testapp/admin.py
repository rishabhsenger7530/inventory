from django.contrib import admin
from .models import User, Product, Sales,OrderProduct,Followupnotes
# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Sales)
admin.site.register(OrderProduct)
admin.site.register(Followupnotes)