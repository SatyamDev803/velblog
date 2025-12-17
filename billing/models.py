from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('PRO', 'Pro'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan_name = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_subscription_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"

    @property
    def is_valid(self):
        if not self.active:
            return False
        if self.end_date and self.end_date < timezone.now():
            return False
        return True

class PaymentHistory(models.Model):
    PAYMENT_GATEWAY_CHOICES = [
        ('STRIPE', 'Stripe'),
        ('RAZORPAY', 'Razorpay'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAY_CHOICES)
    payment_id = models.CharField(max_length=100) # Stripe PaymentIntent ID or Razorpay Payment ID
    order_id = models.CharField(max_length=100, blank=True, null=True) # Razorpay Order ID
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency}"
