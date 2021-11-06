from datetime import date
from dbfread import DBF
import csv

import time

start_time = time.time()
connect_items_csv = open("ConnectItems.csv", "r", newline='')
# connect_items_csv = open("C:/Users/fensk/Documents/GitHub/LPOS_WooCommerce_Inventory_Sync/ConnectItems.csv", "r", newline='')
connect_items = csv.DictReader(connect_items_csv)
connect_items_list = []
for item in connect_items:
    connect_items_list.append(item)

def get_id(item):
    for connection in connect_items_list:
        if connection["sku"] == item["CODE_NUM"].strip():
            return connection["id"]
    return -1

def isEcom(item_type):
    isoList = ["BEER SINGLES", "DEPOSITS", "FREQ", "ICE", "INSTANT", "LOTTO",
               "MISC", "RETURNS", "TOBACCO", "ALLOCATED", ".50 ML & .100 ML",
               ".200/.375 LIQUOR", "SNACKS"]
    tempISOlist = []
    for type in isoList:
        if str.__contains__(item_type, type):
            return False
    for type in tempISOlist:
        if str.__contains__(item_type, type):
            return False
    return True

def make_stock_payload():
    payload = []
    print("Connecting to LPOS database")
    for inv_record in DBF("Z:/LIQCODE.dbf"):
        if isEcom(inv_record["TYPENAM"]):
            if inv_record["LAST_SALE"] == date.today():
                data = {
                    "id": get_id(inv_record),
                    "stock_quantity": inv_record["QTY_ON_HND"]
                }
                payload.append(data)
            elif inv_record["LAST_RCV"] == date.today():
                data = {
                    "id": get_id(inv_record),
                    "stock_quantity": inv_record["QTY_ON_HND"]
                }
                payload.append(data)
    print(round(time.time() - start_time))
    print("found " + str(len(payload)) + " items to update")    
    return payload


def make_update_payload():
    payload = []
    print("Connecting to LPOS database")
    for inv_record in DBF("Z:/LIQCODE.dbf"):
        if isEcom(inv_record["TYPENAM"]):
            if inv_record["LAST_EDIT"] == date.today():
                categories_with_nones = set_dept(inv_record)
                categories = []
                for category in categories_with_nones:
                    if isinstance(category, dict):
                        categories.append(category)
                data = {
                    "id": get_id(inv_record),
                    "name": inv_record["BRAND"] + " " + inv_record["DESCRIP"] + " " + inv_record["SIZE"],
                    "type": "simple",
                    "status": "publish",
                    "sku": inv_record["CODE_NUM"].strip(),
                    "price": str(inv_record["PRICE"]),
                    "regular_price": str(inv_record["PRICE"]),
                    "tax_status": "taxable",
                    "manage_stock": True,
                    "stock_quantity": inv_record["QTY_ON_HND"],
                    "categories": categories,
                }
                if data["id"] != -1:
                    payload.append(data)
    print("found " + str(len(payload)) + " items to update")    
    return payload

def make_new_item_payload():
    payload = []
    print("Connecting to LPOS database")
    database = DBF("Z:/LIQCODE.dbf")
    for inv_record in database:
        if get_id(inv_record) == -1 and isEcom(inv_record["TYPENAM"]):
            categories_with_nones = set_dept(inv_record)
            categories = []
            for category in categories_with_nones:
                if isinstance(category, dict):
                    categories.append(category)
            data = {
                "name": inv_record["BRAND"] + " " + inv_record["DESCRIP"] + " " + inv_record["SIZE"],
                "type": "simple",
                "status": "publish",
                "sku": inv_record["CODE_NUM"].strip(),
                "price": str(inv_record["PRICE"]),
                "regular_price": str(inv_record["PRICE"]),
                "tax_status": "taxable",
                "manage_stock": True,
                "stock_quantity": inv_record["QTY_ON_HND"],
                "categories": categories,
            }
            payload.append(data)
    print("found " + str(len(payload)) + " items to update")    
    return payload

# TODO: This will be taking the information from the "inv_log.dbf" In order to catch any deleted items and 
#       Sending them to WooCommerce
def make_delete_item_payload():
    payload = []
    for inv_record in DBF("Z:/INVLOG.dbf"):
        if inv_record["MODULE"] == "Deleted":
            if inv_record["EDATE"] == date.today():
                print(inv_record["CODE_NUM"])
                payload.append(get_id(inv_record["CODE_NUM"]))
    return payload



def item_create_from_lpos(inv_record, id=-1):
    # TODO: find where the categories are getting nones so we don't have to go thru and find them
    categories_with_nones = set_dept(inv_record)
    categories = []
    for category in categories_with_nones:
        if isinstance(category, dict):
            categories.append(category)
    if id == -1:
        item = {
            "name": inv_record["BRAND"] + " " + inv_record["DESCRIP"] + " " + inv_record["SIZE"],
            "type": "simple",
            "status": "publish",
            "sku": inv_record["CODE_NUM"].strip(),
            "price": str(inv_record["PRICE"]),
            "regular_price": str(inv_record["PRICE"]),
            "tax_status": "taxable",
            "manage_stock": True,
            "stock_quantity": inv_record["QTY_ON_HND"],
            "categories": categories,
        }
    else:
        item = {
            "id": id,
            "name": inv_record["BRAND"] + " " + inv_record["DESCRIP"] + " " + inv_record["SIZE"],
            "type": "simple",
            "status": "publish",
            "sku": inv_record["CODE_NUM"].strip(),
            "price": str(inv_record["PRICE"]),
            "regular_price": str(inv_record["PRICE"]),
            "tax_status": "taxable",
            "manage_stock": True,
            "stock_quantity": inv_record["QTY_ON_HND"],
            "categories": categories,
            "last_sale": inv_record["LAST_SALE"],
            "last_rcv": inv_record["LAST_RCV"],
            "last_edit": inv_record["LAST_EDIT"]
        }
    return item

# branches off to: Beer, Spirit, Misc, or Wine
def set_dept(inv_record):
    categories = []
    if str.__contains__(inv_record['TYPENAM'], "BEER"):
        categories.append({"id": 12680})
        if inv_record['TYPENAM'] != "BEER":
            categories.append(set_beer_varietal(inv_record))
    if not categories:
        for category in set_spirit_type(inv_record):
            categories.append(category)
        if categories:
            categories.append({"id": 21})
    if not categories:
        for category in set_misc_varietal(inv_record):
            categories.append(category)
    if not categories:
        for category in set_wine_varietal(inv_record):
            categories.append(category)
        for category in set_wine_type(inv_record):
            categories.append(category)
        categories.append({"id": 58})
    return categories

def set_beer_varietal(inv_record):
    if inv_record["TYPENAM"] == "BEER- CIDER":
        return {"id": 12681}
    elif inv_record["TYPENAM"] == "BEER- MALT/SELTZER/KOMBUCHA":
        return {"id": 12683}
    elif inv_record["TYPENAM"] == "BEER- MICRO":
        return {"id": 12684}
    elif inv_record["TYPENAM"] == "BEER- NON ALCOHOL":
        return {"id": 12685}
# branches to whiskey or tequila, everything else is covered by this function

def set_spirit_type(inv_record):
    categories = []
    if str.__contains__(inv_record["TYPENAM"], "VODKA"):
        categories.append({"id": 35})
    elif str.__contains__(inv_record["TYPENAM"], "WHIS"):
        categories.append({"id": 22})
        for category in set_whiskey_location(inv_record):
            categories.append(category)
    elif str.__contains__(inv_record["TYPENAM"], "TEQUILA"):
        categories.append({"id": 34})
        for category in set_tequila_varietal(inv_record):
            categories.append(category)
    elif str.__contains__(inv_record["TYPENAM"], "RUM"):
        categories.append({"id": 33})
    elif str.__contains__(inv_record["TYPENAM"], "MOONSHINE"):
        categories.append({"id": 33})
    elif str.__contains__(inv_record["TYPENAM"], "LIQUEUR"):
        categories.append({"id": 31})
    elif str.__contains__(inv_record["TYPENAM"], "GIN"):
        categories.append({"id": 30})
    if str.__contains__(inv_record["TYPENAM"], "BRANDY") or str.__contains__(inv_record["TYPENAM"], "COGNAC"):
        categories.append({"id": 28})
    else:
        pass
    return categories

def set_whiskey_location(inv_record):
    categories = []
    if inv_record["TYPENAM"] == "WHIS-AMERICAN":
        categories.append({"id": 51})
    elif inv_record["TYPENAM"] == "WHIS-CANADIAN":
        categories.append({"id": 52})
    elif inv_record["TYPENAM"] == "WHIS-COLORADO":
        categories.append({"id": 51})
    elif inv_record["TYPENAM"] == "WHIS-IRISH":
        categories.append({"id": 54})
    elif inv_record["TYPENAM"] == "WHIS-JAPANESE":
        categories.append({"id": 55})
    elif inv_record["TYPENAM"] == "WHIS-SCOTCH":
        categories.append({"id": 57})
    if inv_record["DESCRIP"].lower().__contains__("rye"):
        categories.append({"id": 56})
    if inv_record["DESCRIP"].lower().__contains__("burbon"):
        categories.append({"id": 23})
    if inv_record["DESCRIP"].lower().__contains__("redlands"):
        categories.append({"id": 27})
    return categories

def set_tequila_varietal(inv_record):
    categories = []
    if inv_record["DESCRIP"].lower().__contains__("mezcal"):
        categories.append({"id": 49})
    if inv_record["DESCRIP"].lower().__contains__("repo"):
        categories.append({"id": 46})
    if inv_record["DESCRIP"].lower().__contains__("anjeo"):
        if inv_record["DESCRIP"].lower().__contains__("extra"):
            categories.append({"id": 48})
        categories.append({"id": 47})
    if inv_record["DESCRIP"].lower().__contains__("blanc"):
        categories.append({"id": 44})
    if inv_record["DESCRIP"].lower().__contains__("joven"):
        categories.append({"id": 45})
    if inv_record["DESCRIP"].lower().__contains__("cristal"):
        categories.append({"id": 50})
    return categories

# just sets what kinda misc it is.
def set_misc_varietal(inv_record):
    if str.__contains__(inv_record["TYPENAM"], "SNACKS"):
        return[{"id": 90}]
    elif str.__contains__(inv_record["TYPENAM"], "DRINKS"):
        return[{"id": 90}]
    elif str.__contains__(inv_record["TYPENAM"], "GARNISHES"):
        return[{"id": 90}]
    elif str.__contains__(inv_record["TYPENAM"], "MIXES-NON ALCOHOL"):
        return[{"id": 90}]
    else:
        return []

# TODO: I will need to clean wine up and make it cover more edge cases
def set_wine_varietal(inv_record):
    categories = []
    if (inv_record["DESCRIP"]).lower().__contains__("deaux"):
        categories.append({"id": 65})
    elif inv_record["DESCRIP"].lower().__contains__("cab"):
        categories.append({"id": 66})
    elif inv_record["DESCRIP"].lower().__contains__("chard"):
        categories.append({"id": 68})
    elif inv_record["DESCRIP"].lower().__contains__("malbec"):
        categories.append({"id": 69})
    elif inv_record["DESCRIP"].lower().__contains__("merlot"):
        categories.append({"id": 70})
    elif inv_record["DESCRIP"].lower().__contains__("pinot gri"):
        categories.append({"id": 71})
    elif inv_record["DESCRIP"].lower().__contains__("pinot noir"):
        categories.append({"id": 72})
    elif inv_record["DESCRIP"].lower().__contains__("sauv"):
        categories.append({"id": 74})
    elif inv_record["DESCRIP"].lower().__contains__("shiraz"):
        categories.append({"id": 75})
    elif inv_record["DESCRIP"].lower().__contains__("zin"):
        categories.append({"id": 76})
    elif inv_record["TYPENAM"] == "SPARK WINE-AMERICAN" or inv_record["TYPENAM"] == "SPARK WINE-IMPORTED" or inv_record["TYPENAM"] == "CHAMPAGENE":
        categories.append({"id": 67})
    else:
        pass
    return categories

def set_wine_type(inv_record):
    categories = []
    if (inv_record["DESCRIP"]).lower().__contains__("deaux"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("cab"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("chard"):
        categories.append({"id": 60})
    elif inv_record["DESCRIP"].lower().__contains__("malbec"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("merlot"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("pinot gri"):
        categories.append({"id": 60})
    elif inv_record["DESCRIP"].lower().__contains__("pinot noir"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("sauv"):
        categories.append({"id": 60})
    elif inv_record["DESCRIP"].lower().__contains__("shiraz"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("zin"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("rose"):
        categories.append({"id": 62})
    elif inv_record["DESCRIP"].lower().__contains__("red"):
        categories.append({"id": 59})
    elif inv_record["DESCRIP"].lower().__contains__("white"):
        categories.append({"id": 60})
    elif inv_record["TYPENAM"] == "SPARK WINE-AMERICAN" or inv_record["TYPENAM"] == "SPARK WINE-IMPORTED" or inv_record["TYPENAM"] == "CHAMPAGENE":
        categories.append({"id": 61})
    elif inv_record["TYPENAM"] == "SAKE":
        categories.append({"id": 64})
    else:
        pass
    return categories
