from django.contrib import admin

from .models import User
from .models import Clinic
from .models import Token
from .models import Order
from .models import Item
from .models import OrderContainsItem
from .models import PriorityQueue
from .models import DispatchQueue
from .models import Category

admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Token)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderContainsItem)
admin.site.register(PriorityQueue)
admin.site.register(DispatchQueue)
admin.site.register(Category)