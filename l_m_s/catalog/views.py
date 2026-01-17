from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import Book, BookInstance, Author, Genre, Review, ReadingList
from analytics.models import SearchLog, BookPopularity

def book_list(request):
    books = Book.objects.all().select_related('publisher').prefetch_related('authors', 'genres')
    
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(authors__first_name__icontains=search_query) |
            Q(authors__last_name__icontains=search_query) |
            Q(isbn__icontains=search_query)
        ).distinct()
        
        if request.user.is_authenticated:
            SearchLog.objects.create(
                user=request.user,
                search_query=search_query,
                results_count=books.count(),
                ip_address=request.META.get('REMOTE_ADDR')
            )
    
    genre_filter = request.GET.get('genre')
    if genre_filter:
        books = books.filter(genres__id=genre_filter)
    
    language_filter = request.GET.get('language')
    if language_filter:
        books = books.filter(language=language_filter)
    
    sort_by = request.GET.get('sort', 'title')
    if sort_by == 'rating':
        books = books.order_by('-average_rating')
    elif sort_by == 'newest':
        books = books.order_by('-publication_date')
    else:
        books = books.order_by('title')
    
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'genres': Genre.objects.all(),
        'search_query': search_query,
    }
    return render(request, 'catalog/book_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related('publisher')
        .prefetch_related('authors', 'genres', 'instances', 'reviews__user'),
        pk=pk
    )
    
    available_instances = book.instances.filter(status='AVAILABLE').count()
    reviews = book.reviews.all()[:10]
    
    context = {
        'book': book,
        'available_instances': available_instances,
        'reviews': reviews,
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        Review.objects.update_or_create(
            book=book,
            user=request.user,
            defaults={
                'rating': rating,
                'title': title,
                'content': content
            }
        )
        
        reviews = book.reviews.all()
        book.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        book.total_ratings = reviews.count()
        book.save()
        
        return redirect('book_detail', pk=pk)
    
    return render(request, 'catalog/add_review.html', {'book': book})

@login_required
def reading_list_view(request):
    reading_lists = ReadingList.objects.filter(user=request.user).prefetch_related('books')
    return render(request, 'catalog/reading_lists.html', {'reading_lists': reading_lists})

@login_required
def create_reading_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'
        
        ReadingList.objects.create(
            user=request.user,
            name=name,
            description=description,
            is_public=is_public
        )
        return redirect('reading_lists')
    
    return render(request, 'catalog/create_reading_list.html')

def trending_books(request):
    trending = BookPopularity.objects.select_related('book').filter(
        trending_rank__isnull=False
    ).order_by('trending_rank')[:20]
    
    return render(request, 'catalog/trending.html', {'trending_books': trending})
