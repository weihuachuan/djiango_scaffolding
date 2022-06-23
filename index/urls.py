from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings
# from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

app_name = 'index'
urlpatterns = [
    path(r'index/', views.index, name='index'),
]