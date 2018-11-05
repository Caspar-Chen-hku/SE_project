from django.urls import path
from asp import views

urlpatterns = [
	path('clinic_manager/<int:id>/home/<int:category>',
		views.CMViewItems.as_view(),
		name='clinic_manager-home'),
	path('clinic_manager/item_info/<int:id>',
		views.CMViewItemInfo.as_view()),
	path('clinic_manager/construct_order', 
		views.CMConstructOrder.as_view(), 
		name='constructOrder'),
	path('clinic_manager/<int:id>/view_order',
		views.CMViewOrder.as_view(),
		name='clinic_manager-view_order'),
	path('clinic_manager/<int:id>/cancel_order/<int:orderid>',
		views.CMCancelOrder.as_view(),
		name='clinic_manager-cancel-order'),
	path('clinic_manager/<int:id>/confirm_order/<int:orderid>',
		views.CMConfirmOrder.as_view(),
		name='clinic_manager-confirm-order'),
	path('dispatcher/<int:id>/home',
		views.DispatcherViewQueue.as_view(),
		name='dispatcher-home'),
	path('dispatcher/<int:id>/dispatch_order',
		views.DispatcherViewPackage.as_view(),
		name='dispatcher-package'),
	path('dispatcher/generate_csv',
		views.DispatcherViewItinerary.as_view(),
		name='dispatcher-itinerary'),
	path('dispatcher/<int:id>/confirm_dispatch',
		views.DispatcherConfirmDispatch.as_view(),
		name='dispatcher-confirm')
]