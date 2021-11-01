from woocommerce import API
from dbfread import DBF
from datetime import date
import dbf
import csv
import requests

# TODO: get consumer key and consumer secret for api
wcapi = API(
	url="https://redlandsdev.wpengine.com/",
	consumer_key="ck_0efc7fa00dfda4be9d1e2f933b9371768c367f8c",
	consumer_secret="cs_0ded1e8ad3006cee6b05326677a85d018024bb3f",
	version="wc/v3",
	timeout=20
)

# This gets all the orders in processing and sends out a message
# reminding the employees to make delivery.
def get_orders(page = 1):
	sales = wcapi.get("orders?status=processing&page="+ str(page)).json()
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
				data = {
					"name": item["name"],
					"quantity": item["quantity"],
					"sku": item["sku"]
				}
				print(data)
				shopping_cart.append(data)
	
		get_orders(page + 1)

# TODO: This will get all the completed orders, check against
#		
def get_completed_orders(page = 1):
	sales = wcapi.get("orders?status=completed&page="+ str(page)).json()
	new_sales = []
	with open("completed_orders.csv", "r", newline="") as csv_file:
		print("Getting all the completed orders")
		orders_reader = csv.reader(csv_file)
		order_ids = []
		for order in orders_reader:
			order_ids.append(order[0])
	for sale in sales:
		print("Looking for a match for: " + str(sale["id"]))
		already_done = False
		for order in order_ids:
			if order:
				if str(sale["id"]) in order:
					print("This order is already done")
					already_done = True
		if not already_done:
			print("This order needs to be accounted for")
			new_sales.append(sale)
	if new_sales:
		change_lpos_qty(new_sales)
	else:
		print("No new orders, Script over")
			# This is where we get the sku and the quantity sold

# TODO: This will have to take an order that has been completed,
#		and change the master inventory to account for so.
def change_lpos_qty(new_sales):
	LPOS_inv = dbf.Table("Z:/LIQCODE.dbf")
	with open("completed_orders.csv", "a", newline="") as csv_file:
		order_writer = csv.writer(csv_file)
		for sale in new_sales:
			order_writer.writerow([sale["id"]])
			items = sale["line_items"]
			for item in items:
				for thing in dbf.Process(LPOS_inv):
					if item["sku"].strip() == thing["CODE_NUM"].strip():
						new_qty = thing["QTY_ON_HND"] - item["quantity"]
						# thing.QTY_ON_HND = new_qty

get_completed_orders()
