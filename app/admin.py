from django.contrib import admin
from .models import Restaurant, Customer, Order, Item, Payment

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('rname', 'raddress')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cname', 'caddress')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'order_placed_at', 'order_delivered_at', 'order_status', 'restaurant', 'customer', 'order_total')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'iname', 'quantity', 'price', 'itotal')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'items_total', 'packing_charges', 'platform_fee', 'delivery_partner_fee', 'discount_applied', 'taxes',  'order_total')

# Register your models with the custom admin classes
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Payment, PaymentAdmin)
