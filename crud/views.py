from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello World!")

def test(request):
<<<<<<< HEAD
    return render(request, 'layout/base.html')
=======
    return render(request, 'layout/base.html')
>>>>>>> 8f24be39ea1f42ea68e5f527b7a8c06011a7ba3a
