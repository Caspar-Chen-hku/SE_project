from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from datetime import datetime
from django.template import loader
from asp.models import User, Clinic, Token, Order, Item, OrderContainsItem, PriorityQueue, DispatchQueue, Category

def constructOrder(request, id):
	new_order = request.POST['neworder']
	new_weight = request.POST['weight']
	new_priority = request.POST['priority']

	print("new_order: ",new_order)
	print("new_weight: ",new_weight)
	print("new_priority: ",new_priority)

	new_instance = Order.objects.create(weight=new_weight,priority=new_priority,status='QFP',placing_time=datetime.now())
	try:
		new_order = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'http://127.0.0.1:8000/asp/clinic_manager/1/home', {
			'error_message': "modifying database is unsuccessful"
		})
	new_instance.save()
	# Always return an HttpResponseRedirect after successfully dealing
	# with POST data. This prevents data from being posted twice if a
	# user hits the Back button.
	return HttpResponseRedirect(reverse('http://127.0.0.1:8000/asp/clinic_manager/'+id+'/view_order', args=(id)))

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

	#def get(self, request):
	#	return HttpResponse('hello world')

class CMViewItemInfo(ListView):

	template_name = 'asp/view_item_info.html'

	def get_queryset(self):
		self.id = self.kwargs['id']
		return Item.objects.filter(pk=self.id).all()

class CMViewOrder(ListView):
	"""docstring for CMConstructOrder"""
	template_name = 'asp/view_order.html'

	def get_queryset(self):
		self.id = self.kwargs['id']
		return Order.objects.filter(order_id__pk=self.id).all()
		
class DispatcherViewQueue(ListView):
	def get(self, request):
		queue_record_list = DispatchQueue.objects.all()
		order_list = [elem.order_id for elem in queue_record_list]
		template = loader.get_template('asp/dispatch_queue_list.html')
		context = {
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
		return HttpResponse('hello world')

class DispatcherConfirmDispatch(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')