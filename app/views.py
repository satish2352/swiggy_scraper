from django.shortcuts import render, HttpResponse
from .scrap import getEmails
from django.http import HttpResponse
from .models import Restaurant, Customer, Order, Item, Payment
from datetime import datetime
import pytz
from django.db.models import Count, Sum
from .charts_functions import orders_by_status,quantity_by_item, orders_over_time

def get_charttt(request):
    # chart 1
    # status_counts = Order.objects.values('order_status').annotate(count=Count('order_status'))
    # labels = [status['order_status'] for status in status_counts]
    # data = [status['count'] for status in status_counts]

    # Prepare data for JSON response
    chart_data_1 = {
        'labels': labels,
        'data': data,
    }
    # # End of chart 1

    # # chart 2
    # orders_by_status = Order.objects.values('order_status').annotate(count=Count('id'))
    # quantity_by_item = Item.objects.values('iname').annotate(quantity=Sum('quantity'))

    # # Convert the querysets to dictionaries
    # orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
    # quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}

    chart_data_2  = {
        'orders_by_status': orders_by_status_dict,
        'quantity_by_item': quantity_by_item_dict,
    }
     # End of chart 2

    chart_data = {'chart_data_1':chart_data_1,'chart_data_2': chart_data_2}
    return render(request,'app/order_chart.html',{'chart_data': chart_data})

def get_chart(request):
    try:
        chart_data = {
            'chart_1': {'orders_by_status_data': orders_by_status()},
            'chart_2' : {'quantity_by_item_data':quantity_by_item()},
            # 'chart_3' : {'orders_over_time':orders_over_time()}
        }
        print('chart_data----->',chart_data)
        return render(request, 'app/order_chart.html', {'chart_data': chart_data})
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message)
        # return render(request, 'error.html', {'error_message': error_message})

def get_chart_xyz(request):
    try:
        orders_by_status_data = orders_by_status()
        # Chart 1: Order Status Distribution
        # status_counts = Order.objects.values('order_status').annotate(count=Count('order_status'))
        # status_labels = [status['order_status'] for status in status_counts]
        # status_data = [status['count'] for status in status_counts]

        # Chart 2: Orders by Status and Quantity by Item
        
        # quantity_by_item = Item.objects.values('iname').annotate(quantity=Sum('quantity'))

        # Convert querysets to dictionaries
        
        # quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}

        # Prepare data for JSON response
        chart_data = {
            'chart_1': {
                'labels': [orders_by_status_data.keys()], # {'Delivered': 2, 'cancelled': 1}
                'data': [orders_by_status_data.values()]
            }
            }
        #     'chart_1': {
        #         'orders_by_status': orders_by_status_dict,
        #         'quantity_by_item': quantity_by_item_dict,
        #     }
        # }

        print('chart_data',chart_data)

        return render(request, 'app/order_chart.html', {'chart_data': chart_data})
    
    except Exception as e:
        # Handle exceptions gracefully
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})
def scrap_swiggy_data(request):

    return render(request,'app/scrap.html')

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

def chart_data2(request):
    # Query the database for the necessary data
    orders_by_status = Order.objects.values('order_status').annotate(count=Count('id'))
    quantity_by_item = Item.objects.values('iname').annotate(quantity=Sum('quantity'))

    # Convert the querysets to dictionaries
    orders_by_status_dict = {item['order_status']: item['count'] for item in orders_by_status}
    quantity_by_item_dict = {item['iname']: item['quantity'] for item in quantity_by_item}
    print(quantity_by_item)

    chart_data  = {
        'orders_by_status': orders_by_status_dict,
        'quantity_by_item': quantity_by_item_dict,
    }
    # Return the data as a JSON response
    print(chart_data)
    return render(request,'app/order_chart2.html',{'chart_data':chart_data})


    