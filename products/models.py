# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#import the seller object and add the One to many field with the product object
from seller.models import Seller

class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=120, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)#obtain list of objects with respect to the name field(ascending order) 
        verbose_name = 'category'
        verbose_name_plural = 'categories' 

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('category', args=[self.slug])#using view names in URL patterns

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)#One seller has one to many products whereas one product belongs to only one seller
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=150, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)#order product object by if they have been created in descending order
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products-list', args=[self.id, self.slug]) 

