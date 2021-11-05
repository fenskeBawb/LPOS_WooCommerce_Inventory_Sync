from WC_API_Helpers import deploy_batches
from DBF_API_Helpers import *
from WC_API_UpdateConnectItems import update_connect_items

update_payload = make_update_payload()
deploy_batches(update_payload)
new_payload = make_new_item_payload()
deploy_batches(new_payload, "create")
delete_payload = make_delete_item_payload()
deploy_batches(delete_payload, "delete")
update_connect_items()
