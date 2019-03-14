from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("główna strona")

def clients(request):
    return HttpResponse("panel klientów")

def counters(request):
    return HttpResponse("panel liczników")

def units(request):
    return HttpResponse("panel maszyn")
