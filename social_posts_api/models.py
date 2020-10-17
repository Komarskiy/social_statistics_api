from django.core.validators import MinValueValidator
from django.db import models


class PostStatistic(models.Model):
    user_id = models.CharField(max_length=1024)
    post_id = models.CharField(max_length=1024)
    likes_count = models.PositiveBigIntegerField(validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(auto_now_add=True)
