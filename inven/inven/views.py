from django.http import HttpResponse
from django.shortcuts import render

def home_page_view(request):
    context = {
        "page_title" : "Postly"
    }
    return  render(request, "base.html", context)

