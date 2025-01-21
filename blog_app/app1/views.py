from django.shortcuts import render
from .models import Blog

def post_list(request):
    return render(request, 'blog/post_list.html', {})

