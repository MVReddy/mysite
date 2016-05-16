from django.shortcuts import render_to_response, render
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from django.template import RequestContext
 
from .models import DataStore
import xlrd
import xlwt
from django.views.decorators.cache import cache_page
import time
from django.core.cache import cache
from MyCache import RedisCache

# Create your views here.


# @cache_page(60*2, cache='profile', key_prefix="blog")
def home(request):
    s = time.time()
    print "Starting Time: ", s
    reporter = RedisCache.get('1')
    #===========================================================================
    # import pdb
    # pdb.set_trace()
    #===========================================================================
    if not reporter:
        reporter = RedisCache.hydrate_reporter_cahce('1')

    data = {'data': reporter.__dict__}
    e = time.time()
    print "Total Time: ", e-s

    RedisCache.set('n', 'xyz')
    print "Data: ", RedisCache.get('n')

    return render(request, 'myblog/home.html', data)
    # return HttpResponse('Hello World')

