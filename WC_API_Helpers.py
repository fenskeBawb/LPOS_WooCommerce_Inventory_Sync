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
