from django.urls import path
from asp import views

urlpatterns = [
	path('clinic_manager/home',
		views.CMViewItems.as_view(),
		name='clinic_manager-home'),
	path('clinic_manager/construct_order',
		views.CMConstructOrder.as_view(),
		name='clinic_manager-construct'),
	path('dispatcher/home',
		views.DispatcherViewQueue.as_view(),
		name='dispatcher-home'),
	path('dispatcher/dispatch_order',
		views.DispatcherViewPackage.as_view(),
		name='dispatcher-package'),
	path('dispatcher/generate_csv',
		views.DispatcherViewItinerary.as_view(),
		name='dispatcher-itinerary'),
	path('dispatcher/confirm_dispatch',
		views.DispatcherConfirmDispatch.as_view(),
		name='dispatcher-confirm')
]