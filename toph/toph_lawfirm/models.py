from django.db import models

class Entry(models.Model):
    form_id = models.CharField(max_length=255)
    council = models.CharField(max_length=255)
    subject_land_address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    contact_role = models.CharField(max_length=255)
    contact_postal_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    created_date = models.CharField(max_length=255)
    last_updated = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
