from django.urls import path
from asp import views

urlpatterns = [
	path('clinic_manager/<int:id>/home/<int:category>',
		views.CMViewItems.as_view(),
		name='clinic_manager-home'),
	path('clinic_manager/item_info/<int:id>',
		views.CMViewItemInfo.as_view()),
	path('clinic_manager/<int:id>/construct_order', 
		views.constructOrder, 
		name='constructOrder'),
	path('clinic_manager/<int:id>/view_order',
		views.CMViewOrder.as_view(),
		name='clinic_manager-view_order'),
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