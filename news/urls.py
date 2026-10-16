from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.home, name='home'),
    path('news/<slug:slug>/', views.detail, name='detail'),
    path('category/<slug:slug>/', views.category, name='category'),
]
