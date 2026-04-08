from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # 작성자: User 모델과 연결 (사용자 삭제 시 글도 삭제되도록 CASCADE 설정)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # 수정일 추가

    def __str__(self):
        return self.title