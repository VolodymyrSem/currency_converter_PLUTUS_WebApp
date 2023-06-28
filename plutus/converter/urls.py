from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('my_account/', views.my_account_view, name='my_account'),
    path('', views.simple_converter_view, name='converter')
]
