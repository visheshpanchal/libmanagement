from django.db import models


class PDFModel(models.Model):

    pdfname = models.CharField(max_length=64)
    description = models.TextField()
    file = models.FileField()
