# SPEI-Inventory-Tracking-App
For Production Engineer Intern Application

#### Description:

This app is an inventory tracking web application. You are able to:
 - Create Inventory Items
 - Edit Inventory Items
 - Delete Inventory Items
 - View a list of Inventory Items
 - Create Warehouses and assign inventory to them
 - View the city and current weather of the city where item is stored 

#### How to Use:

1. Go to Replit Link: https://replit.com/@Meggin/ProductionEngineer#main.py
2. Click on the blue "Fork repl" button
4. Click "Run" on replit
5. Send Requests by either of the following:
   - Postman:
     - Import postman collection from this Github repository
     - Expand the Shopify Take Home section if necessary
     - In the middle of the page, there is a tab labeled "Variables", click this tab 
     - Set the "CURRENT VALUE" to the domain of your replit
   - Send a curl request, example to create and item is provided. Refer to the Sample Requests for addional requests that can me made using curl.

```
curl -d '{"client_name":"Meggin", "item_name": "Sugars", "warehouse_id": "None", "destination": "FL", "date_aquired": "05/22", "delivery_date": "05/23"}' -H 'Content-Type: application/json' https://INSERT_YOUR_REPLIT_DOMAIN_HERE
```

#### Sample Requests:

To create an item:
  POST: https://INSERT_YOUR_REPLIT_DOMAIN_HERE/create
  
      {
         "client_name":"Meggin",
         "item_name": "Sugars",
         "warehouse_id": "None",
         "destination": "FL",
         "date_aquired": "05/22",
         "delivery_date": "05/23"
      }
      
      
      
To edit an item, including assignment of warehouse:
  POST: https://INSERT_YOUR_REPLIT_DOMAIN_HERE/edit

      {
          "inventory_id": "4",
         "client_name":"Meggin",
         "item_name": "Hairbrush",
         "warehouse_id": "2",
         "destination": "FL",
         "date_aquired": "05/22",
         "delivery_date": "05/23"
      }
    
    
To create a warehouse:
  POST: https://INSERT_YOUR_REPLIT_DOMAIN_HERE/warehouses
  
      {
          "warehouse_name": "NC Triangle",
          "address": "000 Chicken Bridge Road Pittsboro NC 27312",
          "phone": "555-555-5555",
          "capacity": "1000000 Sq Feet",
          "capacity_utilization": "68%"
      }
      
      
To delete an item:
  POST: https://INSERT_YOUR_REPLIT_DOMAIN_HERE/delete

      {
          "inventory_id": "1"
      }


To view the list of items and the city/current weather where that item is stored:
  GET: https://INSERT_YOUR_REPLIT_DOMAIN_HERE/view




#### Technology Stack
   * **Backend:** Python, Flask
   

#### Contact 
Meggin Simon: megginsimon@gmail.com
