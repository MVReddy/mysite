from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    url(r'^home/', views.home, name='home'),
    # url(r'^home/', cache_page(views.home, 60), name='home'),
    ]
