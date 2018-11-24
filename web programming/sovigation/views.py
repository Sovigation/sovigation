# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils import timezone
from sovigation.models import Lib
from sovigation.models import FoodA
from sovigation.models import FoodB
from sovigation.models import FoodC
from sovigation.models import Board
from sovigation.pagingHelper import pagingHelper
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


def board(request):
  boardList = Board.objects.order_by('-id')[0:2]
  current_page = 1
  totalCnt = Board.objects.all().count()
  pagingHelperIns = pagingHelper()
  totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
  print("current_page = "+str(current_page))
  print("totalCnt = "+str(totalCnt))
  print("pagingHelperIns = "+str(pagingHelperIns))
  print("totalPageList = "+str(totalPageList))
  return render_to_response('BoardPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                      'current_page': current_page, 'totalPageList': totalPageList})


def write(request):
  return render_to_response('writeBoard.html')


@csrf_exempt
def dowrite(request):
  br = Board(subject=request.POST['subject'],
             name=request.POST['name'],
             mail=request.POST['email'],
             memo=request.POST['memo'],
             created_date=timezone.now(),
             hits=0
             )
  br.save()
  url = '/board?current_page=1'
  return HttpResponseRedirect(url)


def listpage(request):
  current_page = request.GET['current_page']
  totalCnt = Board.objects.all().count()

  boardList = Board.objects.raw('SELECT Z.* FROM(SELECT X.*, Ceil( count(*) / %s ) as page FROM ( SELECT * '
                                'FROM sovigation_board  ORDER BY ID DESC ) X ) Z WHERE page = %s',
                                [rowsPerPage, current_page])
  print 'boardList=', boardList, 'count()=', totalCnt
  pagingHelperIns = pagingHelper()
  totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
  return render_to_response('BoardPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                               'current_page': int(current_page),
                                               'totalPageList': totalPageList})


def viewwork(request):
  pk = request.GET['memo_id']
  boardData = Board.objects.get(id=pk)
  Board.objects.filter(id=pk).update(hits=boardData.hits + 1)
  return render_to_response('viewMemo.html', {'memo_id': request.GET['memo_id'],
                                              'current_page': request.GET['current_page'],
                                              'searchStr': request.GET['searchStr'],
                                              'boardData': boardData})


def searchedpage(request):
  searchStr = request.GET['searchStr']
  pageForView = request.GET['pageForView']
  totalCnt = Board.objects.filter(subject__contains=searchStr).count()
  pagingHelperIns = pagingHelper()
  totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
  boardList = Board.objects.raw("""SELECT Z.* FROM ( SELECT X.*, Ceil( count(*) / %s) as page FROM ( SELECT * FROM sovigation_board 
                                WHERE SUBJECT LIKE '%%'||%s||'%%' ORDER BY ID DESC) X ) Z WHERE page = %s""",
                                [rowsPerPage, searchStr, pageForView])
  print 'boardList=', boardList, 'count()=', totalCnt
  return render_to_response('SearchedPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                  'pageForView': int(pageForView), 'searchStr': searchStr,
                                                  'totalPageList': totalPageList})


def listupdate(request):
  memo_id = request.GET['memo_id']
  current_page = request.GET['current_page']
  searchStr = request.GET['searchStr']
  boardData = Board.objects.get(id=memo_id)
  return render_to_response('listUpdate.html', {'memo_id': request.GET['memo_id'],
                                                'current_page': current_page,
                                                'searchStr': searchStr,
                                                'boardData': boardData})


@csrf_exempt
def updateboard(request):
    memo_id = request.POST['memo_id']
    current_page = request.POST['current_page']
    searchStr = request.POST['searchStr']
    Board.objects.filter(id=memo_id).update(
                                            mail=request.POST['mail'],
                                            subject=request.POST['subject'],
                                            memo=request.POST['memo']
                                            )
    url = '/board?current_page=' + str(current_page)
    return HttpResponseRedirect(url)


def delete(request):
  memo_id = request.GET['memo_id']
  current_page = request.GET['current_page']
  p = Board.objects.get(id=memo_id)
  p.delete()
  totalCnt = Board.objects.all().count()
  pagingHelperIns = pagingHelper()
  totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
  if int(current_page) in totalPageList:
    current_page = current_page
  else:
    current_page = int(current_page) - 1

  url = '/listPage?current_page=' + str(current_page)
  return HttpResponseRedirect(url)


@csrf_exempt
def searchWithSubject(request):
    searchStr = request.POST['searchStr']
    url = '/searchedPage?searchStr=' + searchStr +'&pageForView=1'
    return HttpResponseRedirect(url)
