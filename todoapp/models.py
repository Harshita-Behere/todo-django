from django.db import models
from django.contrib.auth.models import User

class TODO(models.Model):
    sr = models.AutoField(primary_key = True , auto_created = True)
    title = models.CharField(max_length = 50)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

