from django.urls import path
from . import views

app_name='erp'

urlpatterns=[
    path('<int:id>/',views.item_detail,name='item_detail'),
    path('input_order/',views.input_order,name='input_order'),
    path('output_order/',views.output_order,name='output_order'),
    path('load_subs/',views.load_subs,name='load_subs'),
    path('load_items/',views.load_items,name='load_items'),
    path('search_results_view/',views.search_results_view,name='search_results_view'),
    path('',views.erp_list,name='erp_list'),

    ]