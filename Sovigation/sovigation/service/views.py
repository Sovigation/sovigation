import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from .models import Lib
from .models import FoodA
from .models import FoodB
from .models import FoodC
from .models import UserInfo
from .models import LoginRequest
from .models import LoginResult
from .models import Grade
from .forms import GradeForm
from .pagingHelper import pagingHelper
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import time

rowsPerPage = 5


def index(request):
    return render(request, 'service/index.html')


def about(request):
    return render(request, 'service/about.html')


def assignment(request):
    return render(request, 'service/assignment.html')


def board(request):
    return render(request, 'service/board.html')


def food(request):
    boardListA = FoodA.objects.order_by('-id')[0:6]
    boardListB = FoodB.objects.order_by('-id')[0:6]
    boardListC = FoodC.objects.order_by('-id')[0:6]
    return render_to_response('service/food.html',
                              {'boardListA': boardListA, 'boardListB': boardListB, 'boardListC': boardListC})


def grade(request):
    form = GradeForm()
    return render(request, 'service/grade.html', {'form': form})


def lib(request):
    boardList = Lib.objects.order_by('-id')[0:5]
    return render_to_response('service/lib.html', {'boardList': boardList})


def login(request):
    return render(request, 'service/login.html')


def myService(request):
    return render(request, 'service/myService.html')


def to_do(request):
    return render(request, 'service/to_do.html')


def authenticate(username, password):
    try:
        user = UserInfo.objects.get(username=username, password=password)
    except ObjectDoesNotExist:
        user = None
    return user


def insert_new_user(username, password):
    user = UserInfo(username=username, password=password)
    user.save()


# def insert_grade(request):
#     # if request.method == 'GET':
#     userId = request.session['user']
#     user = UserInfo.objects.get(username=userId)
#     subject = request.GET['_subject']
#     grade = request.GET['_grade']
#     credit = request.GET['_credit']
#     semester = request.GET['_semester']
#     if request.GET['_major'] is 'true':
#         major = True
#     else:
#         major = False
#
#     record = Grade(
#         user=user, grade=grade, credit=credit, semester=semester, major=major, subject=subject
#     )
#     record.save()
#     return render(request, 'servlce/lib.html')
# else:
# return render(request, 'servlce/food.html')

@csrf_exempt
def dologin(request):
    ID = request.POST['username']
    password = request.POST['password']
    lr = LoginRequest(
        name=ID,
        password=password,
    )
    lr.save()

    time.sleep(10)
    try:
        result = LoginResult.objects.get(name=ID)
        if result.result:
            url = '/myservice'
        else:
            url = '/login'
        result.delete()
    except ObjectDoesNotExist:
        url = '/login'
    return HttpResponseRedirect(url)


def board1(request):
  boardList = Board.objects.order_by('-id').all()
  try:
    current_page = request.GET['current_page']
  except:
      current_page = 1
  totalCnt = Board.objects.all().count()
  pagingHelperIns = pagingHelper()
  totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
  boardList = pagingHelperIns.getCurrentPageList(boardList, rowsPerPage, current_page)
  print("rowsPerPage = " + str(rowsPerPage))
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
  boardList = Board.objects.raw("SELECT * FROM sovigation_board WHERE SUBJECT LIKE '%%"+searchStr+"%%' ORDER BY ID DESC")
  print 'searchStr=', searchStr, 'pageForView=', pageForView
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

  url = '/board?current_page=' + str(current_page)
  return HttpResponseRedirect(url)


@csrf_exempt
def searchWithSubject(request):
    searchStr = request.POST['searchStr']
    url = '/searchedPage?searchStr=' + searchStr +'&pageForView=1'
    return HttpResponseRedirect(url)
