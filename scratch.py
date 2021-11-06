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


def display_incomplete_orders(page=1):
    sales = wcapi.get("orders?status=processing&page=" + str(page)).json()
    database = DBF("Z:/LIQCODE.dbf")
    if sales:
        for sale in sales:
			date_created = sale["date_created"].split("T")[0]
			status = sale["status"]
			customer_information = sale["shipping"]
			order_info = sale["line_items"]
			shopping_cart = []
			print(sale["id"])
			for item in order_info:
				data = '''
					There is an order for {delivery_info}
					to the address: {delivery_address}
					contains the following items
				'''.format(delivery_info='delivery', delivery_address='123 Go fuck yourself Avenue')
				# TODO: add the items in as
				#		''' 
				# 			{item_name}
				#			{item_quantity}
				#		'''.format(item_name='',item_quantity='')
				print(items)

				# data = {
				# 	"name": item["name"],
				# 	"quantity": item["quantity"],
				# 	"sku": item["sku"]
				# }

				print(data)
				shopping_cart.append(data)
        display_incomplete_orders(page + 1)

# string = '{} was started in {}'.format(name, year)
