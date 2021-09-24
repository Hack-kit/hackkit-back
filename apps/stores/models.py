from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from model_utils import Choices


class Store(models.Model):
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='업주'
    )


class Food(models.Model):
    CATEGORY_CHOICES = Choices(
        ('vegetables', '야채'),
        ('fruits', '과일'),
        ('meat', '육류'),
        ('fish', '수산'),
        ('etc', '기타')
    )
    store = models.ForeignKey(
        'Store',
        on_delete=models.CASCADE,
        verbose_name='가게명'
    )
    receipt = models.ImageField()
    name = models.CharField(
        max_length=50,
        verbose_name='식자재명'
    )
    food_img = models.ImageField()
    category = models.CharField(
        choices=CATEGORY_CHOICES,
        default=CATEGORY_CHOICES.etc,
        max_length=20,
        verbose_name='음식 카테고리'
    )
    description = models.TextField(
        verbose_name='상세정보'
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0,
        verbose_name='수량'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='등록시간'
    )
    closed_at = models.DateTimeField(
        auto_now=True,
        verbose_name='마감시간'
    )


class Order(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='주문자'
    )
    food = models.ForeignKey(
        'Food',
        on_delete=models.CASCADE,
        verbose_name='식자재'
    )
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0,
        verbose_name='수량'
    )
    ordered_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='주문시간'
    )
    pickup_at = models.DateTimeField(
        auto_now=True,
        verbose_name='픽업시간'
    )
