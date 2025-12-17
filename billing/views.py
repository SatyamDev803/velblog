from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Subscription, PaymentHistory
from django.utils import timezone
import stripe
import razorpay
import json
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def pricing(request):
    return render(request, 'billing/pricing.html')

@login_required
def checkout(request, plan):
    context = {
        'plan': plan,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    }
    
    if plan == 'PRO':
        context['amount'] = 999 
    elif plan == 'ENTERPRISE':
        context['amount'] = 4999
    else:
        return redirect('pricing')
        
    return render(request, 'billing/checkout.html', context)

@login_required
def create_stripe_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plan = data.get('plan')
        
        amount = 99900 if plan == 'PRO' else 499900
        
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'{plan} Subscription',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/billing/success?session_id={CHECKOUT_SESSION_ID}'),
                cancel_url=request.build_absolute_uri('/billing/cancel'),
            )
            return JsonResponse({'sessionId': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@login_required
def create_razorpay_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plan = data.get('plan')
        amount = 99900 if plan == 'PRO' else 499900
        
        order_currency = 'INR'
        order_receipt = f'order_rcptid_{request.user.id}'
        
        try:
            order = razorpay_client.order.create({
                'amount': amount,
                'currency': order_currency,
                'receipt': order_receipt,
                'payment_capture': '1'
            })
            return JsonResponse(order)
        except Exception as e:
             return JsonResponse({'error': str(e)})

@login_required
def payment_success(request):
    # Handle Stripe checkout session
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            # Retrieve the Stripe session
            session = stripe.checkout.Session.retrieve(session_id)
            
            # Get plan from session metadata or line items
            plan_name = 'PRO'  # Default
            amount = session.amount_total / 100 if session.amount_total else 999.00
            
            # Determine plan based on amount
            if amount >= 4999:
                plan_name = 'ENTERPRISE'
            
            # Update or create subscription
            sub, created = Subscription.objects.get_or_create(user=request.user)
            sub.plan_name = plan_name
            sub.active = True
            sub.start_date = timezone.now()
            sub.stripe_subscription_id = session.get('subscription', session.id)
            sub.save()
            
            # Record payment history
            PaymentHistory.objects.create(
                user=request.user,
                amount=amount,
                currency=session.currency.upper() if session.currency else 'INR',
                gateway='STRIPE',
                payment_id=session.payment_intent if session.payment_intent else session.id,
                order_id=session.id,
                status='completed'
            )
            
            messages.success(request, 'Payment successful! Your subscription is now active.')
            
        except stripe.error.StripeError as e:
            messages.error(request, f'Payment verification failed: {str(e)}')
            return redirect('billing:payment_cancel')
        except Exception as e:
            messages.error(request, 'An error occurred. Please contact support.')
            return redirect('billing:payment_cancel')
    
    # Handle Razorpay payment verification
    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    
    if razorpay_payment_id and razorpay_order_id and razorpay_signature:
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Determine plan from request session or amount
            plan_name = 'PRO'  # Default
            amount = 999.00
            
            sub, created = Subscription.objects.get_or_create(user=request.user)
            sub.plan_name = plan_name
            sub.active = True
            sub.start_date = timezone.now()
            sub.razorpay_subscription_id = razorpay_payment_id
            sub.save()
            
            PaymentHistory.objects.create(
                user=request.user,
                amount=amount,
                currency='INR',
                gateway='RAZORPAY',
                payment_id=razorpay_payment_id,
                order_id=razorpay_order_id,
                status='completed'
            )
            
            messages.success(request, 'Payment verified successfully!')
            
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('billing:payment_cancel')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('billing:payment_cancel')
    
    return render(request, 'billing/success.html')

@login_required
def payment_cancel(request):
    return render(request, 'billing/cancel.html')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    # Check if webhook secret is configured
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    
    if not webhook_secret:
        # Log warning but process webhook anyway in development
        # In production, this should return 400
        if not settings.DEBUG:
            return HttpResponse('Webhook secret not configured', status=400)
    
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        else:
            # Development mode: skip signature verification
            event = json.loads(payload)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        
        if customer_email:
            try:
                from django.contrib.auth.models import User
                user = User.objects.get(email=customer_email)
                
                sub, created = Subscription.objects.get_or_create(user=user)
                sub.plan_name = 'PRO'
                sub.active = True
                sub.start_date = timezone.now()
                sub.stripe_subscription_id = session.get('subscription')
                sub.save()
                
                PaymentHistory.objects.create(
                    user=user,
                    amount=session.get('amount_total', 0) / 100,
                    currency=session.get('currency', 'INR').upper(),
                    gateway='STRIPE',
                    payment_id=session.get('payment_intent'),
                    order_id=session.get('id'),
                    status='completed'
                )
                
            except User.DoesNotExist:
                pass
    
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        pass
    
    elif event['type'] == 'invoice.payment_failed':
        pass
    
    return HttpResponse(status=200)
    
@csrf_exempt
def razorpay_webhook(request):
    webhook_secret = settings.RAZORPAY_KEY_SECRET
    webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
    webhook_body = request.body
    
    try:
        razorpay_client.utility.verify_webhook_signature(
            webhook_body.decode('utf-8'),
            webhook_signature,
            webhook_secret
        )
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse(status=400)
    
    event = json.loads(webhook_body)
    event_type = event.get('event')
    
    if event_type == 'payment.captured':
        payment = event['payload']['payment']['entity']
        payment_id = payment.get('id')
        order_id = payment.get('order_id')
        amount = payment.get('amount') / 100
        
        pass
    
    elif event_type == 'payment.failed':
        payment = event['payload']['payment']['entity']
        pass
    
    return HttpResponse(status=200)
