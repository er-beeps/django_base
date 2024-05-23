# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from authentication.models import ActivityLogs, READ, CREATE, UPDATE, DELETE, SUCCESS, FAILED
from django.conf import settings
from master.views import _to_pascalcase

# List of HTTP headers where we will search user IP
IP_ADDRESS_HEADERS = ('HTTP_X_REAL_IP', 'HTTP_CLIENT_IP',
                      'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR')
allowed_app_labels=['master','examination','auth','authentication','course','login','logout']

def get_ip_address(request):
    for header in IP_ADDRESS_HEADERS:
        addr = request.META.get(header)
        if addr:
            return addr.split(',')[0].strip()

class ActivityLogMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    @staticmethod
    def action_type_mapper():
        return {
            "GET": READ,
            "POST": CREATE,
            "PUT": UPDATE,
            "PATCH": UPDATE,
            "DELETE": DELETE,
        }
    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None  
      
    def _get_action_type(self, request) -> str:
        return self.action_type_mapper().get(f"{request.method.upper()}")
    
    def _get_model(self,path):
        url_parts = path.split('/')
        print(url_parts)
        first_string = url_parts[1]
        second_string = url_parts[2] if len(url_parts) > 2 else first_string
        if second_string.isdigit():
            second_string=url_parts[3]
            
        return {'app_label':first_string, 'model':_to_pascalcase(second_string)}
     
    def __call__(self, request):
        
        response = self.get_response(request)
        if settings.ENABLE_ACTIVITY_LOG == 'False':
            return response 
        
        status = SUCCESS if response.status_code < 400 else FAILED
        actor = self._get_user(request)

        app_label= self._get_model(request.path).get('app_label')
        
        if app_label in allowed_app_labels:
            if actor:

                data = {
                    "actor": actor,
                    "request_url":request.build_absolute_uri()[:255],
                    "request_method":request.method,
                    "response_code":response.status_code,
                    "action_type": self._get_action_type(request),
                    "status": status,
                    'ip_address':get_ip_address(request),
                    'model':self._get_model(request.path).get('model')
                }
                ActivityLogs.objects.create(**data)
        
        return response