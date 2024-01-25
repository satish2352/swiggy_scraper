from django.shortcuts import render, HttpResponse
from .scrap import getEmails
from django.http import HttpResponse
from .models import Restaurant, Customer, Order, Item, Payment
from datetime import datetime
import pytz

def scrap_swiggy_data(request):

    return render(request,'app/scrap.html')

# def succssfully_scrap(request): 
#     received_data = getEmails()
#     print(received_data)
#     return HttpResponse("data successfully added")


# views.py


def successfully_scrap(request):
    received_data = getEmails()  # received_data contains the list with data

    for data in received_data:
        # Create and save the Restaurant object
        restaurant = Restaurant.objects.create(
            rname=data['restaurant']['restaurant_name'],
            raddress=data['restaurant']['restaurant_address']
        )

        # Create and save the Customer object
        customer = Customer.objects.create(
            cname=data['customer_info']['customer_name'],
            caddress=data['customer_info']['customer_address']
        )

        # Create and save the Order object
        order = Order.objects.create(
            order_number=data['order_data']['Order No:'],
            order_placed_at=datetime.strptime(data['order_data']['Order placed at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC),
            order_delivered_at=datetime.strptime(data['order_data']['Order delivered at:'], '%A, %B %d, %Y %I:%M %p').replace(tzinfo=pytz.UTC),
            order_status=data['order_data']['Order Status'],
            restaurant=restaurant,
            customer=customer,
            order_total=data['order_summary']['Order Total']
        )

        # Create and save the Item objects
        for item in data['item_details']:
            Item.objects.create(
                order=order,
                iname=item[0],
                quantity=item[1],
                price=item[2],
                itotal=item[1]*item[2]
            )

        # Create and save the Payment object
        Payment.objects.create(
            order=order,
            payment_method='Unknown',  # Update this as per your data
            items_total=data['order_summary']['Item Total'],
            packing_charges=data['order_summary']['Order Packing Charges'],
            platform_fee=data['order_summary']['Platform fee'],
            delivery_partner_fee=data['order_summary']['Delivery partner fee'],
            discount_applied=data['order_summary']['Discount Applied'],
            taxes=data['order_summary']['Taxes'],
            order_total=data['order_summary']['Order Total']
        )

    return HttpResponse("Data successfully added")

    