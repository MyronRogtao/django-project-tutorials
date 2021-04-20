from django.db import models


# Create your models here.
class Realtor(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='realtors')
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateField()

    def __str__(self):
        return self.name
