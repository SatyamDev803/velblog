from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('pricing/', views.pricing, name='pricing'),
    path('checkout/<str:plan>/', views.checkout, name='checkout'),
    path('create-stripe-session/', views.create_stripe_checkout_session, name='create_stripe_session'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('webhook/razorpay/', views.razorpay_webhook, name='razorpay_webhook'),
]
