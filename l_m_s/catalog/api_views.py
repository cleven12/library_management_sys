from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from catalog.models import Book, BookInstance
from circulation.models import Loan
from accounts.models import MemberProfile

@require_http_methods(["GET"])
def api_books_list(request):
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    books = Book.objects.all()
    
    if search:
        books = books.filter(title__icontains=search)
    
    paginator = Paginator(books, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'count': paginator.count,
        'pages': paginator.num_pages,
        'current_page': page,
        'results': [
            {
                'id': book.id,
                'title': book.title,
                'isbn': book.isbn,
                'language': book.language,
                'pages': book.pages,
                'average_rating': float(book.average_rating),
            }
            for book in page_obj
        ]
    }
    
    return JsonResponse(data)

@require_http_methods(["GET"])
def api_book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        data = {
            'id': book.id,
            'title': book.title,
            'subtitle': book.subtitle,
            'isbn': book.isbn,
            'language': book.language,
            'pages': book.pages,
            'description': book.description,
            'average_rating': float(book.average_rating),
            'total_ratings': book.total_ratings,
            'available_copies': book.instances.filter(status='AVAILABLE').count(),
        }
        return JsonResponse(data)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

@login_required
@require_http_methods(["GET"])
def api_my_loans(request):
    try:
        profile = MemberProfile.objects.get(user=request.user)
        loans = Loan.objects.filter(
            member=profile,
            status__in=['ACTIVE', 'OVERDUE']
        ).select_related('book_instance__book')
        
        data = {
            'active_loans': [
                {
                    'id': loan.id,
                    'book_title': loan.book_instance.book.title,
                    'checkout_date': loan.checkout_date.isoformat(),
                    'due_date': loan.due_date.isoformat(),
                    'is_overdue': loan.is_overdue(),
                    'renewal_count': loan.renewal_count,
                    'max_renewals': loan.max_renewals,
                }
                for loan in loans
            ]
        }
        return JsonResponse(data)
    except MemberProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

@require_http_methods(["GET"])
def api_book_availability(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        instances = book.instances.all()
        
        data = {
            'book_id': book.id,
            'book_title': book.title,
            'total_copies': instances.count(),
            'available_copies': instances.filter(status='AVAILABLE').count(),
            'on_loan': instances.filter(status='ON_LOAN').count(),
            'reserved': instances.filter(status='RESERVED').count(),
            'maintenance': instances.filter(status='MAINTENANCE').count(),
        }
        return JsonResponse(data)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
