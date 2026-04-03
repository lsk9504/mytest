from django.db import models

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)  # 제품명
    image = models.ImageField(upload_to='products/')  # 이미지
    description = models.TextField(blank=True, null=True)  # 제품 설명
    expiration_date = models.DateField(blank=True, null=True)  # 유통기한

    def __str__(self):
        return self.name