from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import hashlib

class RateLimitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            ip = request.META.get('REMOTE_ADDR')
            key = f'ratelimit:{ip}'
            
            requests = cache.get(key, 0)
            
            if requests >= 100:
                return JsonResponse({
                    'error': 'Rate limit exceeded. Try again later.'
                }, status=429)
            
            cache.set(key, requests + 1, 60)
        
        return None
