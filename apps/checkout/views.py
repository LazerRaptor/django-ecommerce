from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST',])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, 
        currency='usd',
        payment_method_types=['card',],
        receipt_email='test@example.com',
    )
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)