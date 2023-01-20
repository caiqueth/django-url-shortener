from django.db import models

class UrlRegister(models.Model):
    original_url = models.CharField(max_length=2048)
    new_url = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to="qrcodes")
