from django.urls import path
from .views import test_view, login

urlpatterns = [
    path('test/', test_view, name='test'),
    path('login/', login, name='login')
]