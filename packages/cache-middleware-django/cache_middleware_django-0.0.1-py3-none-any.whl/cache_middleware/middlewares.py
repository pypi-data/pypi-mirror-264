import hashlib
import logging

from django.conf import settings
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

from .utils import remove_cache_by_key

# Create a logger for this file
# Get an instance of a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
    
remove_related_cache = getattr(settings, 'REMOVE_RELATED_CACHE', True)
cache_remove_timeout = getattr(settings, 'CACHE_REMOVE_TIMEOUT', None)
base_api_url = getattr(settings, 'BASE_API_URL', '/api/')
cache_name = getattr(settings, 'CACHE_NAME', settings.ROOT_URLCONF.split('.')[0])

def make_hash(*keys):
    str_keys = [str(key) for key in keys]
    return hashlib.md5("".join(str_keys).encode("utf-8")).hexdigest()

class CacheMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.META['PATH_INFO']  
        
        try:
            module_name = view_func.cls.queryset.model._meta.label_lower
            detail = view_func.initkwargs.get('detail', True)
        except:
            return None
        
        if base_api_url in path and request.method == 'GET' and not detail:
            user_id  = None
            if request.user.is_authenticated:
                user_id = request.user.id
            
            key = make_hash([
                request.get_full_path(),
                request.META.get('HTTP_ACCEPT'),
                user_id])
            
            cache_key = f"{cache_name}-{module_name}:{key}"
            cached_response = cache.get(cache_key)

            if cached_response:
                return cached_response
        return None
    
    def process_response(self, request, response):
        path = request.META['PATH_INFO']  
        
        if not str(response.status_code).startswith('2'):
            return response
        
        try:
            viewset = response.renderer_context['view']
            detail = viewset.detail
            timeout = int(viewset.timeout) if hasattr(viewset, 'timeout') else cache_remove_timeout
            queryset = viewset.queryset or viewset.get_queryset()
            model_meta = queryset.model._meta
            module_name = model_meta.label_lower
            model_fields =  model_meta.get_fields()
        except:
            return response
    
        if base_api_url in path and request.method == 'GET' and not detail:     
            user_id  = None
            if request.user.is_authenticated:
                user_id = request.user.id
            
            key = make_hash([
                request.get_full_path(),
                request.META.get('HTTP_ACCEPT'),
                user_id])
            cache_key = f"{cache_name}-{module_name}:{key}" 

            cache.set(cache_key, response,timeout)                    
        
        elif request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:              
            cache_key = f"{cache_name}-{module_name}:*" 
            remove_cache_by_key(key_name=cache_key)

            if not remove_related_cache:
                return response
            
            for field in model_fields:
                if field.many_to_many or field.many_to_one or field.one_to_many or field.one_to_one:
                    module_name = field.related_model._meta.label_lower

                    cache_key = f"{cache_name}-{module_name}:*" 
                    remove_cache_by_key(key_name=cache_key)
            return response  
        
        return response

