# COMP 3297 Software Engineering Group Project - Air Supply Pilot (ASP)

ASP is a drone-based delivery management system. The deliverable of this project is a single self-contained web application that provides basic ordering, loading planning and route planning services.

The pilot system will serve only a small number of clinics selected from the Southern District and the Islands. Supplies for those clinics will be warehoused and dispatched from Queen Mary Hospital.

## Usage & Limitations

This section specifies some usage rules for the ASP system. Due to time limit or design considerations, there are some limitations in this web applications.

### Clinic Manager:

- To register an account, a clinic manager should select a clinic from seven registered clinics. Currently the web application does not allow a manager add a new clinic.
- A clinic manager cannot select items which weighs more than 23.8 KG. You should not submit the order once you are warned that the total weight exceeds the threshold.

### Warehouse Personnel

- A warehouse personnel should press the "Generate PDF" button to download the shipping label file from the system.
- Since the mail server is not implemented (not required by COMP3297), emails are stored in the file system. In order to send the shipping label to the clinic manager for confirmation, the warehouse personnel should put the file under "sent_emails" folder.
- After the warehouse personnel processes the order, he or she should press the "Confirm" button to notify the system.

### Dispatcher

- A dispatcher should press the "Generate CSV" button to download the itinerary file from the system and upload the file to the drone.
- After the dispatcher dispatches the package to the drone, he or she should press the "Confirm" button to notify the system.

### Other Limitations

- We assume that the warehouse always carries sufficient stock to satisfy all orders. Thus there's no consideration on preventing clinic managers from submitting the order and warehouse personnel from processing the order.
- Each user can only register one account using his or her HA account email.
- There is no need to provide a means to add new medical supplies to the catalogue. All items and their associated data will be added manually by admin.
- There's currently one supplying hospital and one category of supplies. Thus the system does not support hospital management and category management.