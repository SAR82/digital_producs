from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone

from .serializer import PackageSerialiser, SubscriptionSerializer
from .models import Package, Subscription


class PackageView(APIView):
    def get(self, request):
        package = Package.objects.filter(is_enable=True)
        serializer = PackageSerialiser(package, many=True)
        return Response(serializer.data)
    
class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(
            user = request.user,
            expire_time__gt = timezone.now() 
        )
        serializer = SubscriptionSerializer(subscription, many=True)
        return Response(serializer.data)