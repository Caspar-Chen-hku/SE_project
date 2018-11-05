from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from datetime import datetime
from django.template import loader
from asp.models import User, Clinic, Token, Order, Item, OrderContainsItem, PriorityQueue, DispatchQueue, Category
import csv
#def constructOrder(request, id):
#	new_order = request.POST['neworder']
#	new_weight = request.POST['weight']
#	new_priority = request.POST['priority']
#
#	print("new_order: ",new_order)
#	print("new_weight: ",new_weight)
#	print("new_priority: ",new_priority)
#
#	try:
#		new_instance = Order.objects.create(weight=new_weight,priority=new_priority,status='QFP',placing_time=datetime.now())
#	except (KeyError, Choice.DoesNotExist):
#		return render(request, 'http://127.0.0.1:8000/asp/clinic_manager/1/home/1', {
#			'error_message': "modifying database is unsuccessful"
#		})
#	new_instance.save()
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
#	return HttpResponseRedirect(reverse('http://127.0.0.1:8000/asp/clinic_manager/'+id+'/view_order', args=(id)))

class CMConstructOrder(ListView):
	def get(self, request):
		num_order = int(request.GET.get('num',None));
		
		new_weight = float(request.GET.get('weight',None));
		new_priority = request.GET.get('priority',None);
		user_id = int(request.GET.get('user',None));

		new_order = Order();
		new_order.weight=new_weight;
		new_order.priority=new_priority;
		new_order.status='QFP';
		new_order.placing_time=datetime.now();

		user = User.objects.get(pk = user_id)

		new_order.destination_id = user.clinic_id;
		new_order.owner_id = user;

		new_order.save();

		queue = PriorityQueue();
		queue.order_id = new_order;
		queue.save();

		item_list = []
		quantity_list = []
		photo_list = []

		for i in range(num_order):
			new_relation = OrderContainsItem();
			itemid = int(request.GET.get('item'+str(i),None));
			itemnum = int(request.GET.get('item'+str(i)+'num',None));

			item = Item.objects.get(pk=itemid);

			new_relation.order_id = new_order;
			new_relation.item_id = item;
			new_relation.item_quantity = itemnum;

			item_list.append(item.item_name);
			quantity_list.append(itemnum);
			photo_list.append(item.photo_url);

			new_relation.save();

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
	"""docstring for CMViewItems"""
	template_name = 'asp/cm_home.html'

	def get_queryset(self): 
		self.category = self.kwargs['category']
		return Item.objects.filter(category__pk=self.category).all()

	def get_context_data(self, **kwargs): 
		self.id = self.kwargs['id'] 
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id) 
		context['categories'] = Category.objects.all()
		return context

class CMViewItemInfo(ListView):
	template_name = 'asp/view_item_info.html'
	def get_queryset(self):
		self.id = self.kwargs['id']
		return Item.objects.filter(pk = self.id).all()

class CMViewOrder(ListView):
	template_name = 'asp/view_order.html'

	def get_queryset(self):
		self.id = self.kwargs['id']
		return Order.objects.filter(owner_id__pk=self.id).all()

	def get_context_data(self, **kwargs): 
		self.id = self.kwargs['id']
		context = super().get_context_data(**kwargs) 
		context['user'] = User.objects.get(pk = self.id)
		all_orders = Order.objects.filter(owner_id = context['user']).all()

		canceled_orders = [order for order in all_orders if order.status == 'CA']
		normal_orders = [order for order in all_orders if not order.status == 'CA']
		delivered_orders = [order for order in normal_orders if order.status == 'DE']
		processing_orders = [order for order in normal_orders if not order.status == 'DE']
		canceled_orders.extend(delivered_orders)
		context['processing_orders'] = processing_orders
		context['other_orders'] = canceled_orders
		return context
		
class DispatcherViewQueue(ListView):
	def get(self, request):
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		template = loader.get_template('asp/dispatch_queue_list.html')
		username = "James"
		context = {
			'username': username,
			'order_list': order_list,
		}
		return HttpResponse(template.render(context, request))

class DispatcherViewPackage(ListView):
	def get(self, request):
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		total_weight = sum([elem.weight for elem in order_list])
		template = loader.get_template('asp/view_package.html')
		context = {
			'order_list': order_list,
			'total_weight': total_weight,
		}
		return HttpResponse(template.render(context, request))
		
class DispatcherViewItinerary(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		clinic_distance_list= Distance.objects.all()
		clinic_list=Clinic.objects.all()
		distance={}
		#			require Queen Mary's clinic_id be 1
		for elem in clinic_distance_list:
			distance[(elem.source_clinic_id,elem.destination_clinic_id)]=distance[(elem.destination_clinic_id,elem.source_clinic_id)]=elem.distance
		clinic={}
		#require这边clinic_id和上面的对应
		clinic_id=1
		for elem in clinic_list:
			clinic[clinic_id]=(elem.latitude,elem.longitude,elem.altitude)
			clinic_id +=1

		package # a list of order objects
		route_list=[]
		for order in package:
			route_list.append(order.destination_id)
		routes_order=genRoutes(len(route_list),route_list)
		shortest=calCosts(routes_order,distance)
		#with open('itenerary.csv', mode='w') as itenerary_file:
		response = HttpResponse(content_type='text/csv')
		writer=csv.writer(response)
		for item in shortest[0]:
			writer.writerow('latitude longitude and altitude#',clinic[item])
		return response

	def calCosts(routes, distance):
		travelCosts = []

		for route in routes:
			travelCost = 0
			travelCost +=distance[(0,route[0])]
			#Sums up the travel cost
			for i in range(1,len(route)-1):
				#takes an element of route, uses it to find the corresponding coords and calculates the distance
				travelCost += distance[(route[i-1],route[i])]
			travelCosts.append(travelCost)
		#pulls out the smallest travel cost
		smallestCost = min(travelCosts)
		shortest = (routes[travelCosts.index(smallestCost)], smallestCost)
		return shortest


	def genRoutes(routeLength,route_list):
		#uses built-in itertools to generate permutations
		routes = list(map(list, itertools.permutations(route_list)))
		#inserts the home city, must be the first city in every route
		for x in routes:
			x.append(1)
		return routes


class DispatcherConfirmDispatch(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')
