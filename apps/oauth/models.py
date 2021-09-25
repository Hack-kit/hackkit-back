from django.db import models
from model_utils import Choices


class OAuth(models.Model):
    OAUTH_CHOICES = Choices(
        ('Google', 'google'),
        ('default', 'default')
    )
    type = models.CharField(
        choices=OAUTH_CHOICES,
        default=OAUTH_CHOICES.default,
        max_length=10,
        verbose_name='OAuth_Type'
    )
    token = models.CharField(
        db_index=True,
        max_length=255,
        default='',
        verbose_name='OAuth_ID'
    )
