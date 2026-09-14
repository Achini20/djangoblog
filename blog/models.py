from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    Content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.tittle
# Create your models here.
