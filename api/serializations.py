from drf_spectacular import utils
from rest_framework import serializers

from .models import PDFModel


@utils.extend_schema_serializer(exclude_fields=["id"])
class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFModel
        fields = ("id", "pdfname", "description", "file")
