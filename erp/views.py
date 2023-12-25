from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Maincategory,Subcategory,Item,Input_order,Output_order,Company
from .forms import Input_form,Erp_form,Output_form



def item_detail(request,id):
    item=Item.objects.get(id=id)
    return render(request,'erp/item_detail.html',{'item':item})


def input_order(request):
    form=Input_form()
    if request.method=="POST":
        form=Input_form(request.POST)
        if form.is_valid():
            item=form.cleaned_data['item']
            company=form.cleaned_data['company']
            quantity=form.cleaned_data['quantity']
            #주문 자료 저장
            ins_item=Item.objects.get(name=item)
            ins_company=Company.objects.get(name=company)
            input_order=Input_order()
            input_order.item=ins_item
            input_order.company=ins_company
            input_order.quantity=quantity
            input_order.input_stock=ins_item.stock+quantity
            input_order.save()
            #재고 증가
            ins_quantity=ins_item.stock+quantity
            Item.objects.filter(name=item).update(stock=ins_quantity)

            today=datetime.today()
            year = today.year
            month = today.month
            day=today.day
            list=Input_order.objects.filter(created_at__year=year,created_at__month=month,created_at__day=day).order_by('-created_at')
            #filter에 월별 일자별 검색이 안 먹힌다면 timezone 설정 꼭 해줘야 한다.  겁니 짱나네잉


    else:
        list=Input_order.objects.all().order_by('-created_at')
    return render(request, 'erp/input_order.html', {'form':form,'list':list})


def output_order(request):
    form=Output_form()
    if request.method=="POST":
        form=Output_form(request.POST)
        if form.is_valid():
            item=form.cleaned_data['item']
            company=form.cleaned_data['company']
            quantity=form.cleaned_data['quantity']
            #주문 자료 저장
            ins_item=Item.objects.get(name=item)
            if ins_item.stock-quantity>=0:
                ins_company=Company.objects.get(name=company)
                output_order=Output_order()
                output_order.item=ins_item
                output_order.company=ins_company
                output_order.quantity=quantity
                output_order.output_stock=ins_item.stock-quantity
                output_order.save()
                #재고 감소
                ins_quantity=ins_item.stock-quantity
                Item.objects.filter(name=item).update(stock=ins_quantity)

                today=datetime.today()
                year = today.year
                month = today.month
                day=today.day
                list=Output_order.objects.filter(created_at__year=year,created_at__month=month,created_at__day=day).order_by('-created_at')
                #filter에 월별 일자별 검색이 안 먹힌다면 timezone 설정 꼭 해줘야 한다.  겁니 짱나네잉
            else:
                messages.success(request,"재고보다 많이 주문 하셨습니다.")
                list = Output_order.objects.all().order_by('-created_at')

    else:
        list=Output_order.objects.all().order_by('-created_at')
    return render(request, 'erp/output_order.html', {'form':form,'list':list})


def erp_list(request):
    if request.method == "POST":
        form = Erp_form(request.POST)

        if form.is_valid():
            main_category = form.cleaned_data['main_category']  #참고로 request.POST['key']는 값이 없을 때 keyerror를 발생 시킨다. 반면 request.POST.get('키')은 default 반환
            sub_category = form.cleaned_data['sub_category']
            item_name=form.cleaned_data['item']

            main_category = Maincategory.objects.get(name=main_category)
            sub_category = Subcategory.objects.get(category=main_category, name=sub_category)
            item = Item.objects.get(name=item_name,item_category=sub_category, available=True)

            context={
                'item':item,
                'form':form
            }

        else:
            messages.success(request, "해당 아이템이 없습니다!")
            print(form.errors)

    else:
        form = Erp_form()
        items=Item.objects.all()
        context = {
            'items': items,
            'form': form
        }
    return render(request, 'erp/erp_list.html', context)


def load_subs(request):
    main_category_id = request.GET.get("main_category")
    subs = Subcategory.objects.filter(category_id=main_category_id)

    return render(request, "erp/subs_options.html", {"subs": subs})

def load_items(request):
    sub_category_id=request.GET.get("sub_category")
    items=Item.objects.filter(item_category_id=sub_category_id)

    return render(request,"erp/items_options.html",{"items":items})



def search_results_view(request):
    query = request.POST.get('search')  # 해당 키에 해당하는 값이 없으면 None을 리턴, 에러를 일으키진 않는다.

    if query:
        products = Item.objects.filter(name__icontains=query)
    else:
        products = []

    context = {'products': products, 'count': products.count()}
    return render(request, 'erp/search_results.html', context)




"""  날짜 관련 데이터를 찾는 식  created_at이 날짜 데이터를 가지는 필드명일 때
from datetime import datetime

today = datetime.today()

year = today.year
month = today.month
day = today.day

meca = Meca.objects.filter(created_at__year=year, 
created_at__month=month, created_at__day=day)

"""

