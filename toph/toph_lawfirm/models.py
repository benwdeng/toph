from django.db import models

class Entry(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
