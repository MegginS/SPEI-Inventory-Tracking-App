from flask import (Flask, flash, session, redirect, make_response, request, jsonify)
import json
import random
import requests

app = Flask(__name__)


class Item():
    """An item."""

    def __init__(self, inventory_id, client_name, item_name, warehouse_id, city, destination, date_aquired, delivery_date):
      self.inventory_id = inventory_id
      self.client_name= client_name
      self.item_name= item_name
      self.warehouse_id= warehouse_id
      self.city = city
      self.destination= destination
      self.date_aquired= date_aquired
      self.delivery_date= delivery_date

class Warehouse():
  """A Warehouse"""

  def __init__(self, warehouse_id, warehouse_name, address, phone, capacity, capacity_utilization):
    self.warehouse_id = warehouse_id
    self.warehouse_name= warehouse_name
    self.address= address
    self.phone= phone
    self.capacity = capacity
    self.capacity_utilization = capacity_utilization


def verify_attributes(attr1, attr2, attr3, mydict):

    if set((attr1, attr2, attr3)).issubset(mydict.keys()):
       return True
    else:
        return False

def attribute_values(attr_list):

    for attr in attr_list:
        if len(attr) <= 2:
            return False
    return True
        
cities = ["San Francisco, California", "Chambery, France", "Bursa, Turkey", "Astoria, New York", "Pittsboro, North Carolina"]
items = []

def current_weather(city):
    
    payload = {
                'query': city,
                'access_key': '8e00c62c4a51d6b99ebe1184375ba2b3'
                }

    weather_search = requests.get('http://api.weatherstack.com/current', params = payload)
    weather_result = weather_search.json()

    weather_description = str(weather_result['current'].get('weather_descriptions')[0])
    temperature = str(weather_result['current'].get('temperature'))
    weather = "The temperature is " + temperature + " and it is " + weather_description

    return weather

@app.route('/create_items', methods = ['POST'])
def creation():


    if len(items) == 0:
        item_id = 1
    else:
        item_id = items[-1].inventory_id + 1

    item_details= request.get_json()

    attribute_check = verify_attributes("client_name", "item_name", "date_aquired", item_details)
    if attribute_check is False:
        response = {"Status": "Failed", "Error": "Missing Required Attribute"}
        return jsonify(response)


    inventory_id= item_id
    city= random.choice(cities)
    client_name= item_details["client_name"]
    item_name= item_details["item_name"]
    warehouse_id= item_details["warehouse_id"] if "warehouse_id" in item_details else None
    destination= item_details["destination"] if "destination" in item_details else None
    date_aquired= item_details["date_aquired"]
    delivery_date= item_details["delivery_date"] if "delivery_date" in item_details else None


    value = attribute_values([client_name, item_name, city])
    if value is False:
        response = {"Status": "Failed", "Error": "Required attributes must be minimum 2 characters"}
        return jsonify(response)


    item = Item(inventory_id= inventory_id, client_name= client_name, item_name= item_name, warehouse_id= warehouse_id, city = city, destination= destination, date_aquired= date_aquired, delivery_date= delivery_date)

    
    items.append(item)

    response = {"Status": "Success!", "Created": item_name, "Inventory_Id": inventory_id}
    return jsonify(response)


warehouses = []

@app.route('/warehouses_create', methods = ['POST'])
def create_warehouses():
    """Create Warehouses"""

    if len(warehouses) == 0:
        wh_id = 1
    else:
        wh_id = warehouses[-1].warehouse_id + 1

    warehouse_details= request.get_json()

    attribute_check = verify_attributes("warehouse_name", "address", "phone", warehouse_details)
    if attribute_check is False:
        response = {"Status": "Failed", "Error": "Missing Required Attribute"}
        return jsonify(response)

    warehouse_id= wh_id
    warehouse_name= warehouse_details["warehouse_name"]
    address= warehouse_details["address"]
    phone= warehouse_details["phone"]
    capacity= warehouse_details["capacity"] if "capacity" in warehouse_details else None
    capacity_utilization= warehouse_details["capacity_utilization"] if "capacity_utilization" in warehouse_details else None

    value = attribute_values([warehouse_name, address, phone])
    if value is False:
        response = {"Status": "Failed", "Error": "Required attributes must be minimum 2 characters"}
        return jsonify(response)


    warehouse = Warehouse(warehouse_id= warehouse_id, warehouse_name= warehouse_name, address= address, phone= phone, capacity=capacity, capacity_utilization= capacity_utilization)
  
    warehouses.append(warehouse)

    response = {"Status": "Success!", "Created": warehouse_name, "Warehouse_Id": warehouse_id}
    return jsonify(response)


@app.route('/edit_items', methods = ['POST'])
def edit():
    """Edit Items, Assign to Warehouse"""

    edit_request= request.get_json()
    inventory_id= edit_request["inventory_id"]

    if len(items) == 0:
        response = {"Status": "Failed", "Error": "Inventory_ID non existant"}
        return jsonify(response)

    for item in items:

        if item.inventory_id == int(inventory_id):
            item.client_name= edit_request["client_name"]
            item.item_name= edit_request["item_name"]
            item.warehouse_id= edit_request["warehouse_id"]
            item.destination= edit_request["destination"]
            item.date_aquired= edit_request["date_aquired"]
            item.delivery_date= edit_request["delivery_date"]

            response = {"Status": "Success!", "Edited item": inventory_id, "client_name": item.client_name, "item_name": item.item_name, "warehouse_id": item.warehouse_id, "city": item.city, "destination": item.destination, "date_aquired": item.date_aquired, "delivery_date": item.delivery_date}
            return jsonify(response)

    response = {"Status": "Failed", "Inventory_Id": inventory_id, "Error": "Inventory_ID non existant"}
    return jsonify(response)



@app.route('/delete_items', methods = ['POST'])
def delete():
    """Delete Items"""

    delete_request= request.get_json()
    inventory_id= delete_request["inventory_id"]
    
    if len(items) == 0:
        response = {"Status": "Failed", "Error": "Inventory_ID non existant"}
        return jsonify(response)

    for item in items:

        if item.inventory_id == int(inventory_id):
            deleted_item = item
            item_name = item.item_name
            items.remove(deleted_item)
            response = {"Status": "Success!", "Deleted": item_name, "Inventory_Id": inventory_id}
            return jsonify(response)

    response = {"Status": "Failed", "Inventory_Id": inventory_id, "Error": "Inventory_ID non existant"}
    return jsonify(response)



@app.route('/view_items')
def view():
    """View" Items"""

    response = {"Status": "Success!", "Data": []}

    
    for item in items:
        weather = current_weather(item.city)
        response["Data"].append({"inventory_id": item.inventory_id, "item_name": item.item_name, "city": item.city, "weather": weather, "warehouse_id": item.warehouse_id, "client_name": item.client_name, "destination": item.destination, "date_aquired": item.date_aquired, "delivery_date": item.delivery_date})

    return jsonify(response)


@app.route('/')
def home():
    return ('Welcome to my Logistics App')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)