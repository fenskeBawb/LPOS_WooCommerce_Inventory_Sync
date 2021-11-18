from DBF_API_Helpers import *
from woocommerce import API
from dbfread import DBF
# TODO: Write a function to utilize the USER1NAM(varietal) and USER2NAM(region)
#       Use those to make more educated category names

wcapi = API(
	url="https://redlandsdev.wpengine.com/",
	consumer_key="ck_0efc7fa00dfda4be9d1e2f933b9371768c367f8c",
	consumer_secret="cs_0ded1e8ad3006cee6b05326677a85d018024bb3f",
	version="wc/v3",
	timeout=20
)


def do_something():
    pass

# TODO: Write the function for Kacie and her tag names


def kacies_function():
    for item in DBF("Z:/.dbf"):
        pass

# TODO: Write a function that gets all the "processing" orders and posts them for the
#       Cashiers to see
def dis_inc_ord(page=1):
	sales = wcapi.get("orders?status=processing&page=" + str(page)).json()
	if sales:
		delivery_messages = []
		for sale in sales:
			# print(sale)
			#Let's create some strings and then print them in order
			# delivery_info = 'An order has been recieved for: ' +  
			customer_name = sale["shipping"]["first_name"] +' '+ sale["shipping"]["last_name"]
			payment_method = sale["payment_method_title"]
			shipping_address1 = sale['shipping']["address_1"]
			shipping_address2 = sale['shipping']['address_2']
			city = sale['shipping']['city']
			state = sale['shipping']['state']
			zip = sale['shipping']['postcode']
			delivery_message = '''An order for {customer_name} has been found
Please deliver the following items to the address:
{shipping_address1} {shipping_address2}
{city} {state} {zip} 
Cart:\n'''.format(customer_name=customer_name, shipping_address1=shipping_address1, shipping_address2=shipping_address2, city=city, state=state, zip=zip)
			cart = ''
			for product in sale["line_items"]:
				product_name = product["name"]
				quantity = product["quantity"]
				cart = cart + product_name + "\nQuantity: " + str(quantity) + "\n"
			delivery_message += cart
			print(delivery_message)


dis_inc_ord()
# def display_incomplete_orders(page=1):
#     sales = wcapi.get("orders?status=processing&page=" + str(page)).json()
#     database = DBF("Z:/LIQCODE.dbf")
#     if sales:
#         for sale in sales:
# 			print(sale)
# 			# date_created = sale["date_created"].split("T")[0]
# 			# status = sale["status"]
# 			# customer_information = sale["shipping"]
# 			order_info = sale["line_items"]
# 			# shopping_cart = []
# 			print(sale["id"])
# 			for item in order_info:
# 				data = '''
# 				There is an order for {delivery_info}
# 				to the address: {delivery_address}
# 				contains the following items
# 				'''.format(delivery_info='delivery', delivery_address='123 Go fuck yourself Avenue')
# 				# TODO: add the items in as
# 				#		''' 
# 				# 			{item_name}
# 				#			{item_quantity}
# 				#		'''.format(item_name='',item_quantity='')
# 				print(item)

# 				# data = {
# 				# 	"name": item["name"],
# 				# 	"quantity": item["quantity"],
# 				# 	"sku": item["sku"]
# 				# }

# 				print(data)
# 				# shopping_cart.append(data)
    
# 	display_incomplete_orders(page + 1)

# string = '{} was started in {}'.format(name, year)
