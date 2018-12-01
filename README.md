# COMP 3297 Software Engineering Group Project - Air Supply Pilot (ASP)

ASP is a drone-based delivery management system, designed to centralize the medicine supply. The deliverable of this project is a single self-contained web application that provides basic ordering, order processing and dispatching, route planning and other related services.

The pilot system will serve only a small number of clinics selected from the Southern District and the Islands. Supplies for those clinics will be warehoused and dispatched from Queen Mary Hospital.

## Dependencies [IMPORTANT]

- This project is based on the Django framework. Refer to the [Django Tutorial](https://www.djangoproject.com/) to install Django.
- The generation of PDF file depends on the `reportlab` library. Install it using `pip install reportlab`.
- Change the backend mail server to any SMTP server if needed. Currently it's using a file-based backend.

## Usage and Future Release Planning

This section specifies some usage rules for the ASP system. Due to time limit or design considerations, there are some limitations in this web application (ASP).

### Clinic Manager:

- To register an account, a clinic manager should select a clinic from seven registered clinics. Currently the web application does not allow a manager to add a new clinic.
- The weight capacity of drone is 25KG. Excluding the weight of the container, which is 1.2 KG, the maximum weight of any order that a clinic manager can place is 23.8 KG. Any clinic manager will be prevented from submitting the order once you are warned that the total weight exceeds the threshold.
- Once an order is delivered, the clinic manager should click the "delivered" button for the specific order to notify the system

### Warehouse Personnel

- A warehouse personnel should press the "Generate PDF" button to download the shipping label file from the system.
- A warehouse personnel should print and hand the shipping label over to the dispatcher.
- After the warehouse personnel processed the order, he/she should press the "Confirm" button to notify the system.

### Dispatcher

- A dispatcher should press the "Generate CSV" button to download the itinerary file from the system and upload the file to the drone.
- After the dispatcher dispatches the package to the drone, he/she should press the "Confirm" button to notify the system.

### Other Limitations

- We assume that the warehouse always carries sufficient stock to satisfy all orders. Thus there's no consideration on preventing clinic managers from submitting the order and warehouse personnel from processing the order.
- Each user needs to first get a token from the admin before he/she can register as a user. The token should be sent to his/her email address on demand
- Each user can only register one account using his or her HA account email.
- There is no means in the user interface to add new medical supplies to the catalogue. All items and their associated data will be added manually by admin.
- There's currently one supplying hospital (Queen Mary Hospital) and one category of supplies (IV Fluids). Thus the system does not support hospital management and category management.

## Developers

[Haoran Qiu](https://james-qiuhaoran.github.io/index.html), Cheng Chen, Qingqing Li, Shiwen Cao, Xue Wu

## Acknowledgment

The contributors to this project wish to thank [Mr. George Mitcheson](http://www.cs.hku.hk/people/profile.jsp?teacher=georgem) for his generous help and advice throughout this project.

 ## Disclaimer
 
This project has been submitted for partial fulfillment for the course *Software Engineering* offered by University of Hong Kong, 2018-19.
