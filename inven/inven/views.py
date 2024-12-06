from django.http import HttpResponse
from django.shortcuts import render

def home_page_view(request):
    context = {
        "page_title" : "Loyalty"
    }
    return  render(request, "base.html", context)

