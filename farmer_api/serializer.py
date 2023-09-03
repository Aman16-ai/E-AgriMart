from rest_framework import serializers
from account.models import CropDetail

class CropsModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CropDetail
