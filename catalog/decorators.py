from functools import wraps
from django.http import JsonResponse
from catalog.api_models import APIKey
from django.utils import timezone

def require_api_key(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            key_obj.last_used = timezone.now()
            key_obj.save()
            request.api_user = key_obj.user
        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        return func(request, *args, **kwargs)
    
    return wrapper

def paginate_queryset(queryset, page, per_page=20):
    from django.core.paginator import Paginator
    
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page)
    
    return {
        'results': page_obj,
        'count': paginator.count,
        'pages': paginator.num_pages,
        'current_page': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }
