from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from accounts.premium_models import (
    MembershipPlan, Subscription, Payment, Wishlist, Badge, MemberBadge
)
from accounts.models import MemberProfile
import uuid

@login_required
def membership_plans(request):
    plans = MembershipPlan.objects.filter(is_active=True).order_by('price')
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    current_subscription = Subscription.objects.filter(
        member=profile,
        status='ACTIVE'
    ).first()
    
    return render(request, 'accounts/plans.html', {
        'plans': plans,
        'current_subscription': current_subscription
    })

@login_required
def subscribe(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id, is_active=True)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=plan.duration_days)
        
        subscription = Subscription.objects.create(
            member=profile,
            plan=plan,
            status='PENDING',
            start_date=start_date,
            end_date=end_date
        )
        
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        payment = Payment.objects.create(
            member=profile,
            subscription=subscription,
            amount=plan.price,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status='PENDING'
        )
        
        return redirect('process_payment', payment_id=payment.id)
    
    return render(request, 'accounts/subscribe.html', {'plan': plan})

@login_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        payment.status = 'COMPLETED'
        payment.payment_date = timezone.now()
        payment.save()
        
        if payment.subscription:
            payment.subscription.status = 'ACTIVE'
            payment.subscription.save()
            
            payment.member.membership_type = payment.subscription.plan.plan_type
            payment.member.save()
        
        return redirect('subscription_success')
    
    return render(request, 'accounts/payment.html', {'payment': payment})

@login_required
def my_wishlist(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    wishlist_items = Wishlist.objects.filter(
        member=profile
    ).select_related('book').order_by('-priority', '-added_at')
    
    return render(request, 'accounts/wishlist.html', {
        'wishlist_items': wishlist_items
    })

@login_required
def add_to_wishlist(request, book_id):
    from catalog.models import Book
    
    book = get_object_or_404(Book, id=book_id)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    Wishlist.objects.get_or_create(
        member=profile,
        book=book
    )
    
    return redirect('book_detail', pk=book_id)

@login_required
def my_badges(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    earned_badges = MemberBadge.objects.filter(
        member=profile
    ).select_related('badge')
    
    available_badges = Badge.objects.filter(
        is_active=True
    ).exclude(
        id__in=earned_badges.values_list('badge_id', flat=True)
    )
    
    total_points = sum(mb.badge.points for mb in earned_badges)
    
    return render(request, 'accounts/badges.html', {
        'earned_badges': earned_badges,
        'available_badges': available_badges,
        'total_points': total_points
    })

@login_required
def leaderboard(request):
    from django.db.models import Count, Sum
    
    top_readers = MemberProfile.objects.filter(
        status='ACTIVE'
    ).annotate(
        total_loans=Count('loans'),
        total_badges=Count('badges')
    ).order_by('-total_loans')[:50]
    
    return render(request, 'accounts/leaderboard.html', {
        'top_readers': top_readers
    })
