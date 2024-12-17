from django.views.decorators.csrf import csrf_protect
from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

def index(request):
    return render(request, 'charts/index.html', {})
