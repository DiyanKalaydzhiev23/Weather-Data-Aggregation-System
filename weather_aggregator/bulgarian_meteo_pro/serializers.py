from rest_framework import serializers
from .models import BulgarianMeteoProData

class BulgarianMeteoProDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulgarianMeteoProData
        fields = '__all__'
