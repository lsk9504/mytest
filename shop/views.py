import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import register
from django.urls import reverse
from django.views.generic import FormView

from .models import Category, Product, User, Myfile,Mywork,Freeboard,Reply
from cart.forms import CartCountForm

from cart.cart import Cart
import pandas as pd
from plotly.offline import plot
import plotly.express as px
from .forms import Freeboard_Form, Reply_Form,Freeboard_Update_Form
from kshop import settings
from django.core.paginator import Paginator


def product_list(request, category_slug=None):
    category=None
    categories=Category.objects.all()
    products=Product.objects.filter(available=True)
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=products.filter(category=category)
    context={
        'category':category,
        'categories':categories,
        'products':products
    }
    return render(request,'shop/product_list.html',context)


def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_add_form=CartCountForm()
    sale=int(product.price*0.8)
    context={
        'product':product,
        'form':cart_add_form,
        'sale':sale
    }
    return render(request,'shop/product_detail.html',context)


def login_user(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        print("email: ",email,"   password: ",password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('shop:product_list')
        else:
            messages.success(request,"이메일과 비밀번호를 확인 하세요")
            return redirect('shop:login_user')
    else:
        return render(request,'authenticate/login.html',{})



def logout_user(request):
    logout(request)
    return redirect('shop:product_list')


def sign_up(request):

    if request.method=="POST":
        temp_email=request.POST["email"]
        try:
            x=User.objects.get(email=temp_email)
        except:
            x=None
        if x:
            messages.success(request,"이미 있는 이메일 입니다.")
            return redirect('shop:sign_up')
        else:
            user = User()
            user.name=request.POST["name"]
            user.email=request.POST["email"]
            user.phone=request.POST["phone"]
            temp=request.POST["address1"]+ " " +request.POST["address2"]
            user.address=temp
            user.password=request.POST["password"]
            user.set_password(user.password)
            user.save()
            messages.success(request, "가입을 축하 드립니다. 로그인 화면으로 이동 합니다.")
            return redirect('shop:login_user')
    else:
        return render(request,'authenticate/sign_up.html',{})


  # @login_required 는 로그인 하지 않으면 아래 함수를 쓸 수 없고 로그인 화면으로 간다. 감싸는 랩퍼 기능,
  #일일이 if not request.user.is_authenticated ....return redirect() 구문을 안 써도 된다.
  #단, 나는 쓰면 안된다. 정식 경로인 accounts/login 경로를 이용해 작성하지 않았기에!!!
  #또한, 뷰에 클래스로 구현한 구문은 안되며, 함수에서만 사용 가능하다.
def profile_edit(request):
    user=User.objects.get(id=request.user.id)
    if request.method=="POST":
        name=request.POST["name"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        User.objects.filter(id=request.user.id).update(name=name,phone=phone,email=email)
        messages.success(request,"정보를 수정하였습니다")
        return redirect('shop:profile_edit')
    else:
        context={
            'name':user.name,
            'phone':user.phone,
            'email':user.email
        }
        return render(request,'authenticate/profile_edit.html',context)


def find_result(request):
    if request.method=="POST":
        find=request.POST.get('search')
        results=Product.objects.filter(name__icontains=find)
        return render(request,'shop/find_result.html',{'results':results})
    else:
        return render(request,'shop/find_result.html',{})



def file_index(request):

    if request.user.is_authenticated:
        username = request.user.name
    else:
        return redirect('shop:login_user')

    if request.method == "POST":
        subject = request.POST.get("subject")
        myfiles = request.FILES.getlist("file")  #request.FILES['file']는 1개의 파일을 받을 때 getlist와 차이가 있다
        print(subject,"  ",myfiles)
        for i in myfiles:
            Myfile.objects.create(who=username, subject=subject,file=i).save()
        else:
            messages.success(request,"파일을 업로드 하였습니다.")

        files=Myfile.objects.all().order_by('-upload_at')
        return render(request,'shop/file_index.html',{'files':files})
    else:
        files = Myfile.objects.all().order_by('-upload_at')
        return render(request,'shop/file_index.html',{'files':files})


def file_delete(request,id):
    temp=Myfile.objects.get(id=id)
    os.remove(os.path.join(settings.MEDIA_ROOT, str(temp.file))) #media 폴더에 있는 파일 삭제
    temp.delete() #db에 있는 파일 삭제   즉, 데이터베이스와 media 폴더내 파일 2군데를 다 삭제해야 한다.
    messages.success(request,"해당 파일이 삭제 되었습니다.")
    return redirect('shop:file_index')


@register.filter(name='split')
def split(value, key):
    value.split("key")
    return value.split(key)


def index(request):
    qs=Mywork.objects.all()
    projects_data=[
        {
            'Project':x.name,
            'Start':x.start_date,
            'Finish':x.end_date,
            'Responsible':x.responsible.name
        }for x in qs
    ]
    df=pd.DataFrame(projects_data)
    fig=px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Project",
        color="Responsible"
                    )

    fig.update_yaxes(autorange="reversed")
    gantt_plot=plot(fig, output_type="div")
    context={'plot_div':gantt_plot}
    return render(request, 'shop/index.html',context)


#아래는 수작업 페이징 할 때 썼던 코드
# def freeboard(request):
#     freeboards=Freeboard.objects.all()
#     paginator = Paginator(freeboards, 7)  # Show 25 contacts per page.
#
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     context={
#         'page_obj':page_obj
#     }
#     if not freeboards:
#         print('게시글이 없습니다')
#     else:
#         return render(request,'shop/freeboard.html',context)



def freeboard(request):
    freeboards=Freeboard.objects.all()

    context={
        'page_obj':freeboards
    }
    if not freeboards:
        print('게시글이 없습니다')
    else:
        return render(request,'shop/freeboard.html',context)


def freeboard_detail(request,id):
    if not request.user.is_authenticated:
        return redirect('shop:login_user')

    freeboard=Freeboard.objects.get(pk=id)
    if request.user.name==freeboard.writer:
        own='ok'
    else:
        own=None
    reply=Reply.objects.filter(freeboard=freeboard)
    context={
        'freeboard':freeboard,
        'reply':reply,
        'own':own
    }
    return render(request,'shop/freeboard_detail.html',context)

def freeboard_write(request):
    if not request.user.is_authenticated:
        return redirect('shop:login_user')
    else:
        if request.method=="POST":
            form=Freeboard_Form(request.POST, request.FILES) #파일 이동시 html의 form부분에 enctype과 더불어 request.FILES 이지 말기
            if form.is_valid():
                subject=form.cleaned_data['subject']
                content=form.cleaned_data['content']
                image=form.cleaned_data['image']
                temp=Freeboard()
                temp.subject=subject
                temp.content=content
                temp.image=image
                temp.writer=request.user.name
                temp.save()
                return redirect('shop:freeboard')
        else:
            form = Freeboard_Form()
            return render(request,'shop/freeboard_write.html',{'form':form})

"""
def freeboard_update(request,id):   #django의 form을 이용한 업데이트 구문
    temp = Freeboard.objects.get(id=id)

    if request.method=="POST":
        form=Freeboard_Update_Form(request.POST,request.FILES)
        if form.is_valid():
            subject=form.cleaned_data['subject']
            content=form.cleaned_data['content']
            image=form.cleaned_data['image']
            temp.subject=subject
            temp.content=content
            temp.image=image
            temp.save()
            #Freeboard.objects.filter(id=id).update(subject=subject, content=content, image=image, writer=request.user.name)
            #update queryset을 쓰면 imagefield에 upload_to로 지정된 경로에 저정되지 않고 media에 바로 간다.
            #때문에 직접 save() 함수를 이용해 그냥 덮어 써버린다.  명심해야할 건 이건 레코드 추가가 아니고 해당 instance를 업데이트 하는거다.

            messages.success(request, "수정 하였습니다")
            return redirect(reverse('shop:freeboard_update',args=[id]))
        else:
            messages.success(request, "선택 되지 않은 항목이 있습니다")
            return redirect(reverse('shop:freeboard_update',args=[id]))
    init_data = {
        'subject': temp.subject,
        'content': temp.content,
        'image': temp.image
    }
    form = Freeboard_Update_Form(initial=init_data)    #게시판 글 수정 시는 ModelForm을 상속 받아 만들면 instance 속성을 활용해
    context={
        'temp':temp,                                   #손쉽게 썼던 내용을 찾아와 보여줄 수 있다. instance=temp
        'form':form                                    #하지만 forms.Form을 상속 받아 썼다면,initial=사전데이터 형식을 이용해야 한다.
    }
    return render(request,'shop/freeboard_update.html',context)
"""

def freeboard_update(request,id):
    temp = Freeboard.objects.get(id=id)

    if request.method=="POST":
        subject=request.POST.get('subject')
        content=request.POST.get('content')
        image=request.FILES['image']
        temp.subject=subject
        temp.content=content
        temp.image=image
        temp.save()

        return redirect(reverse('shop:freeboard_update',args=[id]))

    context={
        'temp':temp
    }
    return render(request,'shop/freeboard_update.html',context)



def freeboard_delete(request,id):
    temp=Freeboard.objects.get(id=id)
    temp.delete()
    return redirect('shop:freeboard')


def reply_write(request,id):
    if not request.user.is_authenticated:
        return redirect('shop:user_login')

    freeboard = Freeboard.objects.get(pk=id)

    if request.method=="POST":
        content=request.POST.get('content')
        temp=Reply()
        temp.content=content
        temp.writer=request.user.name
        temp.freeboard=freeboard
        temp.save()
    return redirect(reverse('shop:freeboard_detail',args=[freeboard.id]))



