from requests.models import Response
from woocommerce import API

wcapi = API(
	url="https://redlandsdev.wpengine.com/",
	consumer_key="ck_0efc7fa00dfda4be9d1e2f933b9371768c367f8c",
	consumer_secret="cs_0ded1e8ad3006cee6b05326677a85d018024bb3f",
	version="wc/v3",
	timeout=20
)

def dis_inc_ord(page=1):
	sales = wcapi.get("orders?status=processing&page=" + str(page)).json()
	if sales:
		delivery_messages = []
		for sale in sales:
			# print(sale)
			#Let's create some strings and then print them in order
			# delivery_info = 'An order has been recieved for: ' +  
			sale_id = sale["id"]
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
			user_input = input("Please enter: complete/packed\n")
			if user_input.lower().startswith('c'):
				print("Order labeled as completed")
				data = {
					"status": "completed"
				}
				response = wcapi.put("orders/" + str(sale_id), data).json()
	print("No more orders to work on.\nCheck back in after delivery to complete the orders")

dis_inc_ord()