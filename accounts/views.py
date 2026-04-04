from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import MemberProfile, LibrarianProfile, ActivityLog

def register_member(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        member_id = f"MEM{user.id:06d}"
        MemberProfile.objects.create(
            user=user,
            member_id=member_id,
            membership_type='STANDARD'
        )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            ActivityLog.objects.create(
                user=user,
                action='LOGIN',
                details='User logged in successfully',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    ActivityLog.objects.create(
        user=request.user,
        action='LOGOUT',
        details='User logged out',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

@login_required
def profile_view(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    context = {
        'profile': profile,
        'recent_activities': ActivityLog.objects.filter(user=request.user)[:10]
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.bio = request.POST.get('bio', '')
        profile.preferred_genres = request.POST.get('preferred_genres', '')
        profile.save()
        
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        ActivityLog.objects.create(
            user=request.user,
            action='PROFILE_UPDATE',
            details='User updated profile information',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    
    return render(request, 'accounts/profile_edit.html', {'profile': profile})

@login_required
def activity_log_view(request):
    activities = ActivityLog.objects.filter(user=request.user)
    context = {'activities': activities}
    return render(request, 'accounts/activity_log.html', context)
