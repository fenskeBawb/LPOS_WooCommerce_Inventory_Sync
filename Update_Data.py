from WC_API_Helpers import deploy_batches
from DBF_API_Helpers import make_update_payload, make_new_item_payload
from WC_API_UpdateConnectItems import update_connect_items

import time

start_time = time.time()
update_payload = make_update_payload()
deploy_batches(update_payload)
new_payload = make_new_item_payload()
deploy_batches(new_payload, "create")
print("This script took the following time in seconds:")
print(round(time.time() - start_time))
update_connect_items()