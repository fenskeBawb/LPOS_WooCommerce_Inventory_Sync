from woocommerce import API

# This will split the payload into batches and attempt to deploy a payload into batches.
def deploy_batches(payload, deployment_type = "update"):
    wcapi = API(
        url="https://redlandsdev.wpengine.com/",
        consumer_key="ck_0efc7fa00dfda4be9d1e2f933b9371768c367f8c",
        consumer_secret="cs_0ded1e8ad3006cee6b05326677a85d018024bb3f",
        version="wc/v3",
        timeout=20
    )
    batch_size = 25
    batch_count = 0
    if deployment_type == "update":
        batch = {
            "update":[]
        }
        while payload != []:
            if batch_count >= batch_size:
                try:
                    print("Deploying batch")
                    response = wcapi.post("products/batch", batch).json()
                except:
                    deploy_singles(batch, deployment_type, wcapi)
                batch["update"] = []
                batch_count = 0
            else:
                batch_count += 1
                batch["update"].append(payload.pop(0))
        print("Final Batch")
        response = wcapi.post("products/batch", batch).json()
    elif deployment_type == "create":
        batch = {
            "create":[]
        }
        while payload != []:
            if batch_count >= batch_size:
                try:
                    print("Deploying batch")
                    response = wcapi.post("products/batch", batch).json()
                except:
                    deploy_singles(batch, deployment_type, wcapi)
                batch["create"] = []
                batch_count = 0
            else:
                batch_count += 1
                batch["create"].append(payload.pop(0))
            response = wcapi.post("products/batch", batch).json()
            print(response)


# This will be called by deploy_batches if the batch fails. It will take the batch and add each item individually.
def deploy_singles(batch, deployment_type, wcapi):
    print("Deploying batch as singles")
    if deployment_type == "update":
        for inv_record in batch["update"]:
            record_id = inv_record["id"]
            del inv_record["id"]
            response = wcapi.put("products/"+ str(record_id), inv_record.values()).json()
    elif deployment_type == "create":
        for inv_record in batch["create"]:
            response = wcapi.post("products", inv_record).json()

# TODO: This definition doesn't work right now. remove the .csv crap and just have
#       it return the list instead of writing it to a .csv
def find_items_with_no_pics(counter = 0):
	products = wcapi.get("products?per_page=100&page=" + str(counter)).json()
	# get items without a picture and place them into a csv ["name"]["id"]["images"]
	no_pic_items = []
	for product in products:
		if isinstance(product, dict):
			if product["images"] == []:
				data = {
					"name":product["name"],
					"id":product["id"]
				}
				no_pic_items.append(data)
	with open("C:/Users/fensk/Documents/GitHub/RedlandsLiquor/InventorySyncronizer/no_pic_items.csv", "a", newline="") as no_pic_file:
		header = ["name", "id"]
		writer = csv.DictWriter(no_pic_file, header)
		writer.writeheader()
		writer.writerows(no_pic_items)

	if products:
		find_items_with_no_pics(counter + 1)