from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.get_server_list),
    path('state/', views.get_server_state),
    path('house/', views.get_house_data),
    path('sync/', views.sync_data),
    path('sync_ngld/', views.sync_ngld),
    path('captcha/', views.captcha)
]
