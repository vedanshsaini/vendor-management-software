# vendor-management-software
#admin password and username both are vedansh

Create a virtual environment:
cd vendor-management-system
python -m venv venv

Install dependencies:

python manage.py runserver:

API Endpoints
List/Create Vendors:

Endpoint: /vendors/
Methods: GET, POST
Returns a list of vendors or creates a new vendor.
Retrieve/Update/Delete Vendor:

Endpoint: /vendors/<int:pk>/
Methods: GET, PUT, PATCH, DELETE
Retrieves, updates, or deletes a specific vendor by ID.
List/Create Purchase Orders:

Endpoint: /purchase_orders/
Methods: GET, POST
Returns a list of purchase orders or creates a new one.
Retrieve/Update/Delete Purchase Order:

Endpoint: /purchase_orders/<int:pk>/
Methods: GET, PUT, PATCH, DELETE
Retrieves, updates, or deletes a specific purchase order by ID.

Vendor Performance Metrics:

Endpoint: /vendors/<int:vendor_id>/performance/
Method: GET
Retrieves the performance metrics for a specific vendor.


