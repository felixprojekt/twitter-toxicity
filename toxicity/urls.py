from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('insights/', views.insights, name='insights'),
    path('worst_friends/', views.worst_friends, name='worst_friends'),
    path('analyze_tweet/', views.analyze_tweet, name='analyze_tweet'),
    path('<int:user_id>/', views.user_toxicity, name='user_toxicity'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
