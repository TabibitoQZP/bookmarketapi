from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.

def LogIn(request):
    if(request.method=='GET'):
        print(dict(request.GET))
        return JsonResponse(dict(request.GET))
    return HttpResponse('login')
    