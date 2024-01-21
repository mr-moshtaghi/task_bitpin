from django.contrib.auth.models import User
from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ("user", "content")
