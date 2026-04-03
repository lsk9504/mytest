from django.shortcuts import render, get_object_or_404
from .models import Product


def index(request):
    categories=Product.objects.all()

    return render(request,'index.html',{'categories':categories})


def detail(request, pk):
    item = get_object_or_404(Product, pk=pk)
    return render(request, 'detail.html', {'item': item})
