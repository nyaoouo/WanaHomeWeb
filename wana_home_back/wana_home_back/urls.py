from django.http import HttpResponse
from django.urls import path, include, re_path
from django.conf import settings

index_file = (settings.BASE_DIR/"front" / "index.html").read_bytes()

urlpatterns = [
    path('api/', include('api.urls')),
    re_path(r'^.*', lambda x:HttpResponse(index_file)),
]

handler404 = 'api.views.page_not_found'
