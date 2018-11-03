from django.shortcuts import render
from django.views.generic.list import ListView
from asp.models import User, Clinic, Token, Order, Item, OrderContainsItem, PriorityQueue, DispatchQueue
from django.http import HttpResponse

class CMViewItems(ListView):
	"""docstring for CMViewItems"""
	def get(self, request):
		return HttpResponse('hello world')

class CMConstructOrder(ListView):
	"""docstring for CMConstructOrder"""
	def get(self, request):
		return HttpResponse('hello world')
		
class DispatcherViewQueue(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')
		
class DispatcherViewPackage(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')
		
class DispatcherViewItinerary(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')

class DispatcherConfirmDispatch(ListView):
	"""docstring for DispatcherViewQueue"""
	def get(self, request):
		return HttpResponse('hello world')