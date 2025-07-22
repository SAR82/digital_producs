from django.urls import path

from .views import PaymentView, GatewayView

urlpatterns = [
    path('gateways/', GatewayView.as_view()),
    path('pay/', PaymentView.as_view())

]