from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post


# 목록
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})


# 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'board/post_detail.html', {'post': post})


# 작성 (로그인 필요)
@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        # commit=False 대신 바로 생성 시 author 지정
        Post.objects.create(
            title=title,
            content=content,
            author=request.user  # 현재 로그인한 유저 저장
        )
        return redirect('post_list')
    return render(request, 'board/post_create.html')


# 수정 (로그인 필요 & 작성자 확인)
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("수정 권한이 없습니다.")

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'board/post_create.html', {'post': post})


# 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("삭제 권한이 없습니다.")
    post.delete()
    return redirect('post_list')