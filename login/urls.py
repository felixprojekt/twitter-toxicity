from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('result', views.result, name='result'),
    path('info', views.more_info, name='more_info'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
