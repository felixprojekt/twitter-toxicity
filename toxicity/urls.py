from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('<int:user_id>/', views.user_toxicity, name='user_toxicity'),
    path('insights/', views.insights, name='insights'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
