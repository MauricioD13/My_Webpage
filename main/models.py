from django.db import models

# Create your models here.


class Comments(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=70)
    pub_date = models.DateTimeField(auto_now_add=True)
