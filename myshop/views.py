from django.shortcuts import render, get_object_or_404,redirect
from .forms import SignUpForm
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 가입 후 자동 로그인
            return redirect("index")  # 원하는 페이지로 이동
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})