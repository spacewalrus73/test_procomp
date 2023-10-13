from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class Files(models.Model):
    file_name = models.CharField(max_length=255, null=True)
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        upload_to='uploadedfiles/',
        null=False,
    )
