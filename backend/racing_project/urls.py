import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.conf import settings


def react_app(request):
    for base in [settings.STATIC_ROOT, os.path.join(settings.BASE_DIR, 'static')]:
        index_path = os.path.join(base, 'index.html')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                return HttpResponse(f.read(), content_type='text/html')
    return HttpResponse(
        '<html><body style="font-family:sans-serif;padding:40px;text-align:center">'
        '<h2>🏆 EdgeBet Pro</h2><p>App is initializing, please refresh in a moment.</p></body></html>',
        content_type='text/html'
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('races.urls')),
    re_path(r'^.*$', react_app),
]
