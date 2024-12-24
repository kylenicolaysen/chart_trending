from django.views.decorators.csrf import csrf_protect
from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from charts.chart_gen.chart_gen import main

def index(request):
    return render(request, 'charts/index.html', {})

def generate(request):
    tickers_list = [ticker.strip() for ticker in request.POST['tickers'].split(',')]
    print('TICKER LIST IN VIEW.PY: ', tickers_list)
    group_title = request.POST['group title']
    hist_length = request.POST['number of total days']
    interval = request.POST['interval']
    main(tickers_list, group_title, hist_length, interval)
    return HttpResponseRedirect(reverse('charts:chart_display', args=([])))

def chart_display(request):
    return render(request, 'charts/display.html', {'image_list': []})