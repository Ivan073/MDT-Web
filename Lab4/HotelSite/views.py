from django.shortcuts import render
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("test2")

# Create your views here.
