from rest_framework import serializers

from .models import Gateways

class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateways
        fields = ('id', 'title', 'description', 'avatar')