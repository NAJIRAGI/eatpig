from django.db import models

from account.models import Account


# Create your models here.

class Content(models.Model):
    contents = models.TextField()  # 글 내용
    image = models.TextField()  # 글 안의 음식 사진
    diner = models.CharField(max_length=100)  # 식당 이름 정보
    region = models.CharField(max_length=100)  # 지역 정보
    menu = models.CharField(max_length=100)  # 메뉴 정보
    user = models.ForeignKey(Account, on_delete=models.CASCADE)


class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)


class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    reply_content = models.TextField()


class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_marked = models.BooleanField(default=True)
