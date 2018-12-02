# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'service/index.html')


def about(request):
    return render(request, 'service/about.html')


def assignment(request):
    return render(request, 'service/assignment.html')


def board(request):
    return render(request, 'service/board.html')


def food(request):
    return render(request, 'service/food.html')


def grade(request):
    return render(request, 'service/grade.html')


def lib(request):
    return render(request, 'service/lib.html')


def login(request):
    return render(request, 'service/login.html')


def myService(request):
    return render(request, 'service/myService.html')


def to_do(request):
    return render(request, 'service/to_do.html')
