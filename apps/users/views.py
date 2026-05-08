from django.shortcuts import render
from django.http import JsonResponse

# 나중에 옮길 것
def index(request):
    return render(request, 'index.html')

def test_view(request):
    return JsonResponse({"message": "Hello, World!"})
