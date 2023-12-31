"""
URL configuration for kshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/',include('django_summernote.urls')),
    path('shop/',include('shop.urls')),
    path('cart/',include('cart.urls')),
    path('erp/',include('erp.urls')),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='authenticate/password_reset_form.html'),name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='authenticate/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='authenticate/password_reset_complete.html'),name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
