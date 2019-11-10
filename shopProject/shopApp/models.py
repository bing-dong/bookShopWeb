from django.db import models

# Create your models here.

# 用户
class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name
# 书
class Book(models.Model):
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='img')
    price = models.IntegerField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.name
# 购物车
class Cart(models.Model):
    user = models.CharField(max_length=128)
    book = models.CharField(max_length=128)
    count = models.IntegerField()

    def __str__(self):
        return self.user
# 历史记录
class History(models.Model):
    user = models.CharField(max_length=128)
    book = models.CharField(max_length=128)

    def __str__(self):
        return self.user