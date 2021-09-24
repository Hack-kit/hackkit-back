from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

from model_utils import Choices

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    # 일반 유저 생성
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    # 관리자 유저 생성
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        return self._create_user(email, password, **kwargs)


class Address(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='가게명'
    )
    # location = PointField


class User(AbstractUser):
    USER_CHOICES = Choices(
        ('owner', '업주'),
        ('customer', '고객')
    )
    oauth = models.OneToOneField(
        'oauth.OAuth',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='oauth'
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='이메일'
    )
    phone = PhoneNumberField()
    address = models.OneToOneField(
        'Address',
        on_delete=models.CASCADE,
        verbose_name='주소'
    )
    user_type = models.CharField(
        choices=USER_CHOICES,
        default=USER_CHOICES.owner,
        max_length=10,
        verbose_name='사용자 타입'
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Review(models.Model):
    customer = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name='고객'
    )
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0,
        verbose_name='수량'
    )
    content = models.TextField()
