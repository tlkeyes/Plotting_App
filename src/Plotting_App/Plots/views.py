from django.shortcuts import render

# Create your views here.

def home_view(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'Plots/base.html', context)

def about_view(request):
    context = {
        'title': 'About'
    }
    return render(request, 'Plots/about.html', context)