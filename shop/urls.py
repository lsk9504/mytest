from django.urls import path
from . import views
app_name='shop'

urlpatterns=[
    path('index/',views.index,name='index'),
    path('freeboard/',views.freeboard,name='freeboard'),
    path('freeboard_detail/<int:id>/',views.freeboard_detail,name='freeboard_detail'),
    path('freeboard_write/',views.freeboard_write,name='freeboard_write'),
    path('freeboard_delete/<int:id>/',views.freeboard_delete,name='freeboard_delete'),
    path('freeboard_update/<int:id>/',views.freeboard_update,name='freeboard_update'),
    path('reply_write/<int:id>/',views.reply_write,name='reply_write'),
    path('find_result/',views.find_result,name='find_result'),
    path('file_index/',views.file_index,name='file_index'),
    path('file_delete/<int:id>/',views.file_delete,name='file_delete'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('<str:category_slug>/',views.product_list,name='product_list_category'),
    path('<int:id>/<str:slug>/',views.product_detail,name='product_detail'), #한글일때는 <str:slug>방식을 쓴다.
    path('',views.product_list,name='product_list'),


]