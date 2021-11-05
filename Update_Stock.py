from WC_API_Helpers import deploy_batches
from DBF_API_Helpers import make_stock_payload
from WC_API_GetOrders import get_completed_orders

get_completed_orders()
qty_payload = make_stock_payload()
print("payload completed, deploying now...")
deploy_batches(qty_payload)
print("This script took the following time in seconds:")
