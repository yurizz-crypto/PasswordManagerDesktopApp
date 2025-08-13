from django.db import models
from django.conf import settings

class PasswordEntry(models.Model):
    user = models.ForeignKey(settings.AUT)