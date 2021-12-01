from django.db import models


class PdfTemplate(models.Model):
    file = models.BinaryField()
