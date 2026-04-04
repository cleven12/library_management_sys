import time
from django.utils.deprecation import MiddlewareMixin
from accounts.models import ActivityLog

class ActivityLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request, 'start_time'):
                duration = time.time() - request.start_time
                
                if duration > 1.0:
                    ActivityLog.objects.create(
                        user=request.user,
                        action='SLOW_REQUEST',
                        details=f'{request.method} {request.path} took {duration:.2f}s',
                        ip_address=request.META.get('REMOTE_ADDR')
                    )
        
        return response

class RequestTimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            response['X-Request-Duration'] = f'{duration:.3f}'
        return response
