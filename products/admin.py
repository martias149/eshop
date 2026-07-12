from django.contrib import admin
from .models import (
    Brand, Category, Product, ProductImage,
    Customer, Address, Order, OrderItem, Review, Cart, CartItem,
)

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
