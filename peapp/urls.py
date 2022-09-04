from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    path('exam/<int:topic_id>/', views.exam, name='exam'),
    path('results/', views.results, name='results'),
    path('my_results/', views.my_results, name='my_results'),
    path('favourites/', views.favourites, name='favourites'),
    path('about/', views.about, name='about'),
    path('logout', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('topics/', views.topics, name='topics'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)