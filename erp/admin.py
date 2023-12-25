from django.contrib import admin
from .models import Maincategory,Subcategory,Item,Company,Input_order,Output_order


admin.site.register(Maincategory)
admin.site.register(Subcategory)
admin.site.register(Item)
admin.site.register(Company)
admin.site.register(Input_order)
admin.site.register(Output_order)
