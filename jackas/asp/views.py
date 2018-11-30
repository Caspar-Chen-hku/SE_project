import itertools, csv, io, os, tsp, math
from django.contrib.auth.models import User as DjangoUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from datetime import datetime
from django.template import loader
from django.http import HttpResponseRedirect
from asp.models import User, Clinic, Token, Order, Item, OrderContainsItem, PriorityQueue, DispatchQueue, Category, Distance
from django.shortcuts import redirect
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from django.core.mail import EmailMessage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

class HomePage(ListView):
	def get(self,request):
		template = loader.get_template('asp/homepage.html')
		num_user = len(User.objects.all())
		context = {
			'num_user': num_user
		}
		return HttpResponse(template.render(context, request))

class ViewHome(ListView):
	def get(self,request):
		userid = int(request.GET.get('id',None))
		role = request.GET.get('role',None)

		if role == 'CM':
			category_id = Category.objects.get(category_name='IV Fluids').pk
			return redirect('/asp/clinic_manager/'+str(userid)+'/home')
		elif role == 'D':
			return redirect('/asp/dispatcher/'+str(userid)+'/home')
		else:
			return redirect("/asp/warehouse_personnel/"+str(userid)+"/home")		

class PersonalHome(ListView):
	def get(self, request):

		name = request.user.username
		user = User.objects.get(username = name)
		userid = user.pk

		context = {}

		if user.role == 'CM':
			category_id = Category.objects.get(category_name='IV Fluids').pk
			return redirect('/asp/clinic_manager/'+str(userid)+'/home')
		elif user.role == 'D':
			return redirect('/asp/dispatcher/'+str(userid)+'/home')
		else:
			return redirect("/asp/warehouse_personnel/"+str(userid)+"/home")

class PersonalInfo(ListView):
	template_name = 'asp/personal_info.html'

	def get_queryset(self): 
		self.id = self.kwargs['id']
		return User.objects.filter(pk=self.id).all()

class ChangeInfo(ListView):
	def get(self, request):
		username = request.GET.get('username',None)

		firstname = request.GET.get('firstname',None)
		lastname = request.GET.get('lastname',None)
		email = request.GET.get('email',None)
		password = request.GET.get('password',None)

		target_user = User.objects.get(username=username)

		target_user.firstname = firstname
		target_user.lastname = lastname
		target_user.email = email

		django_user = DjangoUser.objects.get(username=target_user.username)

		django_user.first_name = firstname
		django_user.last_name = lastname
		django_user.email = email
		django_user.set_password(password)
		
		target_user.password = password

		target_user.save()

		django_user.save()
		return redirect('/asp/'+str(target_user.pk)+'/personal_info')


class CMConstructOrder(ListView):
	def get(self, request):
		num_order = int(request.GET.get('num',None))
		
		new_weight = float(request.GET.get('weight',None))
		new_priority = request.GET.get('priority',None)
		user_id = int(request.GET.get('user',None))

		new_order = Order()
		new_order.weight=new_weight
		new_order.priority=new_priority
		new_order.status='QFP'
		new_order.placing_time=datetime.now()

		user = User.objects.get(pk = user_id)

		new_order.destination_id = user.clinic_id
		new_order.owner_id = user

		new_order.save()

		queue = PriorityQueue()
		queue.order_id = new_order
		queue.save()

		item_list = []
		quantity_list = []
		photo_list = []

		for i in range(num_order):
			new_relation = OrderContainsItem()
			itemid = int(request.GET.get('item'+str(i),None))
			itemnum = int(request.GET.get('item'+str(i)+'num',None))

			item = Item.objects.get(pk=itemid)

			new_relation.order_id = new_order
			new_relation.item_id = item
			new_relation.item_quantity = itemnum

			item_list.append(item.item_name)
			quantity_list.append(itemnum)
			photo_list.append(item.photo_url)

			new_relation.save()

		template = loader.get_template('asp/view_order_info.html')
		context = {
			'num_order': num_order,
			'new_weight': new_weight,
			'new_priority': new_priority,
			'user_id': user_id,
			'item_list': item_list,
			'quantity_list': quantity_list,
			'photo_list': photo_list
		}
		return HttpResponse(template.render(context, request))


class CMViewItems(ListView):
	template_name = 'asp/cm_home.html'

	def get_queryset(self):
		categories = Category.objects.all()
		self.category = categories[0]
		return Item.objects.filter(category=self.category).all()

	def get_context_data(self, **kwargs): 
		self.id = self.kwargs['id'] 
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id) 
		context['categories'] = Category.objects.all()
		categories = Category.objects.all()
		context['cat'] = categories[0]
		return context

class CMViewItemInfo(ListView):
	template_name = 'asp/view_item_info.html'
	def get_queryset(self):
		self.id = self.kwargs['id']
		return Item.objects.filter(pk = self.id).all()

class CMViewShippingLabel(ListView):
	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type='application/pdf')
		self.order_id = self.kwargs['id']
		order = Order.objects.get(pk=self.order_id)

		filename = "shipping_label-" + str(order.pk) + ".pdf"

		response['Content-Disposition'] = 'attachment; filename=' + filename
		
		Order_Item = OrderContainsItem.objects.all()

		destination = Clinic.objects.get(pk=order.destination_id.pk)
		p = canvas.Canvas(response)
		p.setTitle("Shipping Label - ASP")
		p.drawString(100, 800, 'OrderNumber: ' + str(order.pk))

		p.drawString(300, 800, 'Priority: ' + str(order.priority))
		p.drawString(100, 750, 'Order info:')
		length=730
		for elem in Order_Item:
			if elem.order_id == order:
				item_name = Item.objects.get(pk=elem.item_id.pk).item_name
				p.drawString(100, length, 'Item Name: ' + str(item_name)+'    Quantity: '+str(elem.item_quantity))
				length=length-20
		p.drawString(100, length-20, 'Destination: ' + str(destination.clinic_name))
		p.drawString(100, length-40, 'Address: '+str(destination.clinic_address))
		p.showPage()
		p.save()

		return response

class CMViewOrder(ListView):
	template_name = 'asp/view_order.html'

	def get_queryset(self):
		self.id = self.kwargs['id']

	def get_context_data(self, **kwargs): 
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id)
		all_orders = Order.objects.filter(owner_id = context['user']).all()

		canceled_orders = [order for order in all_orders if order.status == 'CA']
		normal_orders = [order for order in all_orders if not order.status == 'CA']
		delivered_orders = [order for order in normal_orders if order.status == 'DE']
		processing_orders = [order for order in normal_orders if not order.status == 'DE']
		canceled_orders.extend(delivered_orders)

		for order in processing_orders:
			order.status = order.get_status_display()
			order.priority = order.get_priority_display()
		for order in canceled_orders:
			order.status = order.get_status_display()
			order.priority = order.get_priority_display()

		context['processing_orders'] = processing_orders
		context['other_orders'] = canceled_orders
		return context

class CMCancelOrder(ListView):
	def get(self, request, *args, **kwargs):
		self.id = kwargs['id']
		self.orderid = kwargs['orderid']
		order_to_update = Order.objects.get(id=self.orderid)
		order_to_update.status = 'CA'
		order_to_update.canceled_time = datetime.now()
		order_to_update.save()
		order_to_remove_from_queue = PriorityQueue.objects.get(order_id = order_to_update)
		order_to_remove_from_queue.delete()
		return redirect('/asp/clinic_manager/'+str(self.id)+'/view_order')

class CMConfirmOrder(ListView):
	def get(self, request, *args, **kwargs):
		self.id = kwargs['id']
		self.orderid = kwargs['orderid']
		order_to_update = Order.objects.get(id=self.orderid)
		order_to_update.status = 'DE'
		order_to_update.dilivered_time = datetime.now()
		order_to_update.save()
		return redirect('/asp/clinic_manager/'+str(self.id)+'/view_order')

class DispatcherViewQueue(ListView):
	template_name = 'asp/dispatch_queue_list.html'

	def get_queryset(self):
		self.id = self.kwargs['id']

	def get_context_data(self, **kwargs): 
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id)
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		for order in order_list:
			order.priority = order.get_priority_display()
		context['order_list'] = reorderQueue(order_list)
		return context

def calculatePackage(reordered_list):
	package = []
	total_weight = 0
	i = 0
	while total_weight <= 25 and i < len(reordered_list):
		package.append(reordered_list[i])
		total_weight += float(reordered_list[i].weight) + float(1.2)
		i += 1
		if i >= len(reordered_list):
			break
		elif total_weight + float(reordered_list[i].weight) + float(1.2) > 25:
			break	
	return package

class DispatcherViewPackage(ListView):
	template_name = 'asp/view_package.html'

	def get_queryset(self):
		self.id = self.kwargs['id']

	def get_context_data(self, **kwargs): 
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id)
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		reordered_list = reorderQueue(order_list)

		package = calculatePackage(reordered_list)
		total_weight = sum([elem.weight for elem in package])
		context['order_list'] = package
		context['total_weight'] = str(total_weight) + " + 1.2 * " + str(len(package)) + " = " + str(round(float(total_weight)+len(package)*1.2,2))
		return context
		
class DispatcherViewItinerary(ListView):
	MAXIMUM = 10000
	def get(self, request):
		# generate package
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]

		reordered_list = reorderQueue(order_list)
		package = calculatePackage(reordered_list) #package is essentially an order list
		clinic_list = [order.destination_id for order in package]
		print(clinic_list)

		#clinics include hospital as the first element
		clinics = [(22.270257,22.270257,161,0)]
		for i in range(len(clinic_list)):
			clinics.append((clinic_list[i].latitude, clinic_list[i].longitude, clinic_list[i].altitude, clinic_list[i].distance_to_hospital))
		
		distance = self.calDistance(clinic_list)
		print(distance)

		#result is in the form of (cost, list of indices)
		shortest = self.genRoute(distance)

		response = HttpResponse(content_type='text/csv')
		output_name = 'itinerary'
		file_ext = 'csv'
		response['Content-Disposition'] = 'attachment; filename="itenerary.csv"'
		
		writer = csv.writer(response)
		writer.writerow(['latitude', 'longitude', 'altitude'])
		for item in shortest[1][1:]:
			writer.writerow([clinics[item][0],clinics[item][1],clinics[item][2]])

		# final destination should be the hospital
		writer.writerow(["22.270257", "22.270257", "161"])
		return response

	def calDistance(self,clinic_list):
		distance = {}

		distance[(0,0)] = 0.0
		for i in range(len(clinic_list)):
			distance[(0,i+1)] = float(clinic_list[i].distance_to_hospital)

		for i in range(len(clinic_list)):
			distance[(i+1,0)] = float(clinic_list[i].distance_to_hospital)
			for j in range(len(clinic_list)):
				if j == i:
					distance[(i+1,j+1)] = 0.0
				else:
					target = Distance.objects.filter(source_clinic_id__pk = clinic_list[i].pk, destination_clinic_id__pk = clinic_list[j].pk)
					for elem in target:
						distance[(i+1,j+1)] = float(elem.distance)
		return distance

	def genRoute(self, distance):
		r = range(int(math.sqrt(len(distance))))
		print("r is: "+str(r))
		# dist = {(i, j): distance[i][j] for i in r for j in r}
		return tsp.tsp(r, distance)

class DispatcherConfirmDispatch(ListView):
	def get(self, request, *args, **kwargs):
		self.id = kwargs['id']
		
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]

		reordered_list = reorderQueue(order_list)
		package = calculatePackage(reordered_list)
		for order in package:
			order_to_update = Order.objects.get(pk=order.pk)
			order_to_update.status = 'DI'
			order_to_update.dispatching_time = datetime.now()
			order_to_update.dispatcher_id = User.objects.get(pk = self.id)
			order_to_update.save()
			order_to_remove_from_queue = DispatchQueue.objects.get(order_id = order)
			order_to_remove_from_queue.delete()

			to_addr = order_to_update.owner_id.email
			owner_name = order_to_update.owner_id.firstname
			subject = 'Your order ' + str(order.pk) + ' is dispatched! - ASP'
			body = "Dear " + str(owner_name) + ",\n\nYour order has been dispatched.\n\n" \
					"\n\nOrder ID: " + str(order.pk) + "" \
					"\nDispatched Time: " + str(order_to_update.dispatching_time) + "" \
					"\nDispatched by: " + str(order_to_update.dispatcher_id.username) + "" \
					"\n\nAttached you can see the shipping lable as your reference. Thanks for using ASP!\n" \
					"\nOr see the file here: http://127.0.0.1:8000/asp/clinic_manager/shipping_label/" + str(order.pk)
			from_addr = 'admin@asp.com'
			email = EmailMessage(
				subject,
				body,
				from_addr,
				[to_addr],
			)
			attachment = open(EMAIL_FILE_PATH+"\\shipping_label-"+str(order.pk)+".pdf", 'rb')
			email.attach("shipping_label-"+str(order.pk)+".pdf",attachment.read(),'application/pdf')
			email.send(fail_silently=False)
		
		return redirect('/asp/dispatcher/'+str(self.id)+'/home')

def reorderQueue(order_list):
	high_orders = []
	medium_orders = []
	low_orders = []

	for order in order_list:
		order.priority = order.get_priority_display()
		if order.priority == "High":
			high_orders.append(order)
		elif order.priority == "Medium":
			medium_orders.append(order)
		else:
			low_orders.append(order)
		order.status = order.get_status_display()
	order_to_display = []
	order_to_display.extend(high_orders)
	order_to_display.extend(medium_orders)
	order_to_display.extend(low_orders)
	return order_to_display

class WarehousePersonnelHome(ListView):
	template_name = 'asp/priority_queue_list.html'
	def get_queryset(self):
		self.id = self.kwargs['id']
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.get(pk=self.id)
		priority_queue_record_list = PriorityQueue.objects.all()
		order_list = [elem.order_id for elem in priority_queue_record_list]
		order_to_display = reorderQueue(order_list)

		context['order_list'] = order_to_display
		return context

class WarehousePersonnelProcessOrder(ListView):
	template_name = 'asp/wp_process_order.html'
	def get_queryset(self):
	   self.id = self.kwargs['id']

	# viewing the details of the order removed for packing with name,quantity,destination
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.get(pk = self.id)

		priority_queue_record_list = PriorityQueue.objects.all()
		order_list = [elem.order_id for elem in priority_queue_record_list]
		order_to_display = reorderQueue(order_list)

		order_to_process = order_to_display[0]
		item_list = OrderContainsItem.objects.filter(order_id=order_to_process).all()
		context['order'] = order_to_process
		context['item_list'] = item_list

		# update the database to processing state
		order_to_update = Order.objects.get(pk=order_to_process.pk)
		order_to_update.status = 'PBW'
		order_to_update.processing_time = datetime.now()
		order_to_update.processor_id = User.objects.get(pk=self.id)
		order_to_update.save()
		return context

class WarehousePersonnelConfirmOrder(ListView):
	def get(self, request, *args, **kwargs):
		self.id = kwargs['id']
		queue_record_list = PriorityQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		
		order_to_display = reorderQueue(order_list)

		order = order_to_display[0]

		order_to_confirm=Order.objects.get(pk=order.pk)
		order_to_confirm.status = 'QFD'
		order_to_confirm.processing_time = datetime.now()
		order_to_confirm.processor_id = User.objects.get(pk = self.id)
		order_to_confirm.save()
		order_to_remove_from_queue = PriorityQueue.objects.get(order_id = order)
		order_to_remove_from_queue.delete()
		queue = DispatchQueue();
		queue.order_id = order;
		queue.save();

		return redirect('/asp/warehouse_personnel/'+str(self.id)+'/home')

class WarehousePersonnelGenerateSL(ListView):
	
	# need to install reportlab
	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type='application/pdf')
		
		queue_record_list = PriorityQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		
		order_to_display = reorderQueue(order_list)

		order = order_to_display[0]
		order_to_update = Order.objects.get(pk=order.pk)

		filename = "shipping_label-" + str(order.pk) + ".pdf"

		response['Content-Disposition'] = 'attachment; filename=' + filename
		
		Order_Item = OrderContainsItem.objects.all()

		destination = Clinic.objects.get(pk=order.destination_id.pk)
		p = canvas.Canvas(response)
		f = canvas.Canvas(EMAIL_FILE_PATH+"\\"+filename)
		print(EMAIL_FILE_PATH+"\\"+filename)
		p.setTitle("Shipping Label - ASP")
		p.drawString(100, 800, 'OrderNumber: ' + str(order.pk))
		p.drawString(300, 800, 'Priority: ' + str(order.priority))
		p.drawString(100, 750, 'Order info:')
		length=730
		for elem in Order_Item:
			if elem.order_id == order:
				item_name = Item.objects.get(pk=elem.item_id.pk).item_name
				p.drawString(100, length, 'Item Name: ' + str(item_name)+'    Quantity: '+str(elem.item_quantity))
				f.drawString(100, length, 'Item Name: ' + str(item_name)+'    Quantity: '+str(elem.item_quantity))
				length=length-20
		p.drawString(100, length-20, 'Destination: ' + str(destination.clinic_name))
		p.drawString(100, length-40, 'Address: '+str(destination.clinic_address))
		p.showPage()
		p.save()
		f.setTitle("Shipping Label - ASP")
		f.drawString(100, 800, 'OrderNumber: ' + str(order.pk))
		f.drawString(300, 800, 'Priority: ' + str(order.priority))
		f.drawString(100, 750, 'Order info:')
		f.drawString(100, length-20, 'Destination: ' + str(destination.clinic_name))
		f.drawString(100, length-40, 'Address: '+str(destination.clinic_address))
		f.showPage()
		f.save()

		return response