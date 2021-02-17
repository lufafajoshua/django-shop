from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from user_profiles.models import Profile
from products.models import Product


class OrderItem(models.Model):#inheriting the product model object and using it in the order object 
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)#orderitem extends the product model object (inherits the product model)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(default=1)#Set One as a default for the quantity and the user can update if they need more that one
    price = models.DecimalField(max_digits=7, decimal_places=2)#

    def update_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    """Get the total cost of the prodcut with a given quantity"""
    def update_price(self):
        self.price = self.quantity * self.product.price
        self.save

    def total_cost(self):
        return self.quantity * self.price    

    def __str__(self):
        return self.product.name

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)#an orderitem can be on multple ordes and an order has many orderitems
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price * item.quantity for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)


class Transaction(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # token = models.CharField(max_length=120)
    order_id = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=65, decimal_places=2)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

class ShippingInfo(models.Model):
    email = models.EmailField()
    address = models.CharField(max_length=200)#relationship with the shipping information
    telephone = models.CharField(max_length=30)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)#One order has only one shipping Info, and one shipping info belongs to only one order

    # class Sold_Orders(models.Model):
    #     products = models.ManyToManyField(Order)#get the quantity and the seller from this relationship
    #     selling_date = models.DateField(auto_now=True)#Automatically create this athe time of transaction
    #     #total = models.IntegerField(default=0)# Sold_Product.objects.count(), This gives the total number of products sold

    #     def total(self):#This returns all the sold products in a given period of time
    #         return self.objects.count()


    


        