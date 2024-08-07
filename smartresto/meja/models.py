from django.db import models

# Create your models here.
class Meja(models.Model):
    id = models.AutoField(primary_key=True)
    nama_meja = models.CharField(max_length=50)
    status = models.CharField(max_length=255)