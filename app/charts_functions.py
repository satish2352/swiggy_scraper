from .models import Restaurant, Customer, Order, Item, Payment
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay


def orders_by_status():
    orders_by_status = Order.objects.values('order_status').annotate(count=Count('id'))
    orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
    return orders_by_status_dict

def quantity_by_item():
    quantity_by_item = Item.objects.values('iname').annotate(quantity=Sum('quantity'))
    quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}
    return quantity_by_item_dict

def orders_over_time():
        # import library TruncDay
        data = Order.objects.annotate(date=TruncDay('order_placed_at')).values('date').annotate(c=Count('id')).values('date', 'c')
        # print(data)
        return data