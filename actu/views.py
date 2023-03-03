from django.shortcuts import render,redirect, get_object_or_404
from actu.models import Blog, Category

# Create your views here.


def view_post(request, slug):   
   return render(request,'view_post.html', {
       'post': get_object_or_404(Blog, slug=slug)
})

def view_category(request, slug):
   category = get_object_or_404(Category, slug=slug)
   return render(request,'view_category.html', {
       'category': category,
       'posts': Blog.objects.filter(category=category)[:5]
})