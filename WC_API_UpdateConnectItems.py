from woocommerce import API
import csv

def update_connect_items():
	wcapi = API(
		url="https://redlandsdev.wpengine.com/",
		consumer_key="ck_0efc7fa00dfda4be9d1e2f933b9371768c367f8c",
		consumer_secret="cs_0ded1e8ad3006cee6b05326677a85d018024bb3f",
		version="wc/v3",
		timeout=20
	)

	csv_file = open("ConnectItems.csv", "w", newline="")
	connected_items = csv.writer(csv_file)
	header = ["id", "sku"]
	connected_items.writerow(header)
	recursive_update(wcapi, connected_items)
	csv_file.close()

def recursive_update(wcapi, writer, counter=1):
	products = wcapi.get("products?per_page=100&page=" + str(counter)).json()
	if products:
		for product in products:
			stripped_item = {
				"id": product["id"],
				"sku": product["sku"]
			}
			writer.writerow(stripped_item.values())
		print(str(round(counter/.95, 2)) + "%% complete")
		recursive_update(wcapi, writer, counter+1)

update_connect_items()

