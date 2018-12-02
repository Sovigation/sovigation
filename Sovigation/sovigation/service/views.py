# Create your views here.
from django.shortcuts import render


def login(request):
  return render('service/login.html', {})


def about(request):
  return render('service/about.html', {})


def assignment(request):
  return render('service/assignment.html', {})


def board(request):
  return render('service/board.html', {})


def contact(request):
  return render('contact.html', {})


def food(request):
  return render('food.html', {})


def index(request):
  return render('index.html', {})


def grade(request):
  return render('grade.html', {})


def lib(request):
  return render('lib.html', {})


def myservice(request):
  return render('myService.html', {})


def todo(request):
  return render('to_do.html', {})
