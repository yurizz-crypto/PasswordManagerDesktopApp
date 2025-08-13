from django.db import models
from django.conf import settings

class PasswordEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=255)
    site_url = models.URLField(blank=True, null=True)
    username = models.CharField(max_length=255)
    encrypted_password = models.TextField()
    notes = models.TextField(blank=True)