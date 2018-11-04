from django.shortcuts import render
from django.views.generic.list import ListView
from asp.models import User, Clinic, Token, Order, Item, OrderContainsItem, PriorityQueue, DispatchQueue
from django.http import HttpResponse
from django.template import loader

class CMViewItems(ListView):
	"""docstring for CMViewItems"""
	def get(self, request):
		return HttpResponse('hello world')

class CMConstructOrder(ListView):
	"""docstring for CMConstructOrder"""
	def get(self, request):
		return HttpResponse('hello world')
		
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