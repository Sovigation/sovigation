# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils import timezone
from sovigation.models import Lib
from sovigation.models import FoodA
from sovigation.models import FoodB
from sovigation.models import FoodC
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
rowsPerPage = 5

def lib(request):
  boardList = Lib.objects.order_by('-id')[0:5]
  return render_to_response('libPage.html', {'boardList': boardList})


def fooda(request):
  boardList = FoodA.objects.order_by('-id')[0:6]
  return render_to_response('foodaPage.html', {'boardList': boardList})


def foodb(request):
  boardList = FoodB.objects.order_by('-id')[0:6]
  return render_to_response('foodbPage.html', {'boardList': boardList})


def foodc(request):
  boardList = FoodC.objects.order_by('-id')[0:6]
  return render_to_response('foodcPage.html', {'boardList': boardList})


def home(request):
    return render_to_response('home.html', {})