from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'blog/home.html', {'title': 'home'})

def about(request):
    return render(request, 'blog/about.html', {'tittle':'about'})

def contact(request):
    return render(request, 'blog/contact.html', {'tittle':'contact'})
