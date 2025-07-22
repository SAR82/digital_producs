from rest_framework import serializers

from .models import Package, Subscription


class PackageSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('title', 'sku', 'description', 'avatar', 'price', 'duration')

class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerialiser()
    class Meta:
        model = Subscription
        fields = ('package', 'created_time', 'expire_time')
