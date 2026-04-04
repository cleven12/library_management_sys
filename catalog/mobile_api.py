from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catalog.models import Book, BookInstance
from circulation.models import Loan, Fine, Reservation
from accounts.models import MemberProfile
from catalog.serializers import BookSerializer, LoanSerializer, FineSerializer
from django.utils import timezone
from datetime import timedelta

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mobile_dashboard(request):
    """Mobile app dashboard with user stats and quick actions"""
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    active_loans = Loan.objects.filter(
        member=profile,
        status__in=['ACTIVE', 'OVERDUE']
    ).count()
    
    pending_fines = Fine.objects.filter(
        member=profile,
        status='PENDING'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    active_reservations = Reservation.objects.filter(
        member=profile,
        status='ACTIVE'
    ).count()
    
    return Response({
        'user': {
            'username': request.user.username,
            'full_name': request.user.get_full_name(),
            'membership_type': profile.membership_type,
        },
        'stats': {
            'active_loans': active_loans,
            'pending_fines': float(pending_fines),
            'active_reservations': active_reservations,
        }
    })

@api_view(['GET'])
def mobile_book_search(request):
    """Optimized book search for mobile"""
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    per_page = 10
    
    books = Book.objects.filter(
        title__icontains=query
    ).select_related('publisher')[:per_page * page]
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'results': serializer.data,
        'page': page,
        'has_more': books.count() == per_page * page
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mobile_scan_book(request):
    """Scan book barcode and get info"""
    barcode = request.data.get('barcode')
    
    if not barcode:
        return Response(
            {'error': 'Barcode required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        instance = BookInstance.objects.select_related('book').get(
            barcode=barcode
        )
        
        return Response({
            'book': {
                'id': instance.book.id,
                'title': instance.book.title,
                'isbn': instance.book.isbn,
                'status': instance.status,
            }
        })
    except BookInstance.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mobile_quick_checkout(request):
    """Quick checkout for mobile librarian app"""
    member_id = request.data.get('member_id')
    barcode = request.data.get('barcode')
    
    try:
        member = MemberProfile.objects.get(member_id=member_id)
        instance = BookInstance.objects.get(barcode=barcode)
        
        if instance.status != 'AVAILABLE':
            return Response(
                {'error': 'Book not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from circulation.models import CheckoutPolicy
        
        policy = CheckoutPolicy.objects.filter(
            membership_type=member.membership_type
        ).first()
        
        due_date = timezone.now().date() + timedelta(
            days=policy.loan_period_days if policy else 14
        )
        
        loan = Loan.objects.create(
            book_instance=instance,
            member=member,
            due_date=due_date,
            checked_out_by=request.user
        )
        
        instance.status = 'ON_LOAN'
        instance.save()
        
        return Response({
            'success': True,
            'loan_id': loan.id,
            'due_date': due_date.isoformat()
        })
        
    except (MemberProfile.DoesNotExist, BookInstance.DoesNotExist) as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mobile_notifications(request):
    """Get mobile notifications"""
    from notifications.models import Notification
    
    notifications = Notification.objects.filter(
        user=request.user,
        status__in=['PENDING', 'SENT']
    ).order_by('-created_at')[:20]
    
    return Response({
        'notifications': [
            {
                'id': n.id,
                'type': n.notification_type,
                'title': n.title,
                'message': n.message,
                'created_at': n.created_at.isoformat(),
            }
            for n in notifications
        ]
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mobile_renew_loan(request, loan_id):
    """Renew loan from mobile"""
    loan = get_object_or_404(Loan, id=loan_id)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    if loan.member != profile:
        return Response(
            {'error': 'Not authorized'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if loan.renewal_count >= loan.max_renewals:
        return Response(
            {'error': 'Maximum renewals reached'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    from circulation.models import CheckoutPolicy, RenewalHistory
    
    policy = CheckoutPolicy.objects.filter(
        membership_type=profile.membership_type
    ).first()
    
    old_due_date = loan.due_date
    new_due_date = old_due_date + timedelta(
        days=policy.loan_period_days if policy else 14
    )
    
    RenewalHistory.objects.create(
        loan=loan,
        old_due_date=old_due_date,
        new_due_date=new_due_date,
        renewed_by=request.user
    )
    
    loan.due_date = new_due_date
    loan.renewal_count += 1
    loan.save()
    
    return Response({
        'success': True,
        'new_due_date': new_due_date.isoformat(),
        'renewals_remaining': loan.max_renewals - loan.renewal_count
    })
