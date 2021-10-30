from WC_API_Helpers import deploy_batches
from DBF_API_Helpers import make_stock_payload

import time

start_time = time.time()
qty_payload = make_stock_payload()
print("payload completed, deploying now...")
deploy_batches(qty_payload)
print("This script took the following time in seconds:")
print(round(time.time() - start_time))