from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Create your views here.
def index(request):
     if request.user.is_authenticated:
          return render(request,"main/index.html",{"autenticado": True,"nombre": request.user.username})
     return render(request,"main/index.html")

