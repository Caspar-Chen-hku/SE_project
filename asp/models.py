from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	password = models.CharField(max_length=20)
	email = models.CharField(max_length=50)

    ROLE_CHOICES = (
        ('CM', 'Clinic Manager'),
        ('WP', 'Warehouse Personnel'),
        ('D', 'Dispacher'),
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default='CM',
    )
	def __str__(self):
		return self.username

class Clinic(models.Model):
	clinic_name = models.CharField(max_length=100)
	clinic_address = models.CharField(max_length=200)
	def __str__(self):
		return self.clinic_name

class Token(models.Model):
	token_string = models.CharField(max_length=6, min_length=6)
	user_role = models.CharField(max_length=2)
	def __str__(self):
		return self.token_string

class Order(models.Model):
	owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	PRIORITY_CHOICES = (
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=1,
    )
	STATUS_CHOICES = (
        ('QFP', 'Queued for Processing'),
        ('PBW', 'Processing by Warehouse'),
        ('QFD', 'Queued for Dispatch'),
        ('DI', 'Dispatched'),
        ('DE', 'Delivered'),
        ('CA', 'Canceled')
    )
    status = models.CharField(
    	max_length=3
        choices=STATUS_CHOICES,
        default='QFP',
    )
    placing_time = models.DateTimeField()
    processing_time = models.DateTimeField()
    processor_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    dispatching_time = models.DateTimeField()
    dispatcher_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    dilivered_time = models.DateTimeField()
    canceled_time = models.DateTimeField()
    destination = models.CharField(max_length=200)
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
	def __str__(self):
		return f'{self.placing_time} ({self.status})'

class Item(models.Model):
	item_name = models.CharField(max_length=150)
	item_description = models.CharField(max_length=250)
	photo_url = models.CharField(max_length=200)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	category = models.CharField(max_length=50)
	def __str__(self):
		return self.item_name

class OrderContainsItem(models.Model):
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
	item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.order_id} ({self.item_id})'

class PriorityQueue(models.Model):
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
	def __init__(self):
		return self.order_id

class DispatchQueue(models.Model):
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
	def __init__(self):
		return self.order_id