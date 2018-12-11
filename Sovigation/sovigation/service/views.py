# Create your views here.
import logging

logger = logging.getLogger(__name__)
from django.shortcuts import render, redirect
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
from .models import Board
from .pagingHelper import pagingHelper
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import time


rowsPerPage = 5


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
            url = '/myService'
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
    print("current_page = " + str(current_page))
    print("totalCnt = " + str(totalCnt))
    print("pagingHelperIns = " + str(pagingHelperIns))
    print("totalPageList = " + str(totalPageList))
    return render_to_response('service/BoardPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                         'current_page': current_page, 'totalPageList': totalPageList})


def write(request):
    return render_to_response('service/writeBoard.html')


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
    print
    'boardList=', boardList, 'count()=', totalCnt
    pagingHelperIns = pagingHelper()
    totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
    return render_to_response('service/BoardPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                         'current_page': int(current_page),
                                                         'totalPageList': totalPageList})


def viewwork(request):
    pk = request.GET['memo_id']
    boardData = Board.objects.get(id=pk)
    Board.objects.filter(id=pk).update(hits=boardData.hits + 1)
    return render_to_response('service/viewMemo.html', {'memo_id': request.GET['memo_id'],
                                                        'current_page': request.GET['current_page'],
                                                        'searchStr': request.GET['searchStr'],
                                                        'boardData': boardData})


def searchedpage(request):
    searchStr = request.GET['searchStr']
    pageForView = request.GET['pageForView']
    totalCnt = Board.objects.filter(subject__contains=searchStr).count()
    pagingHelperIns = pagingHelper()
    totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
    boardList = Board.objects.raw(
        "SELECT * FROM sovigation_board WHERE SUBJECT LIKE '%%" + searchStr + "%%' ORDER BY ID DESC")
    print
    'searchStr=', searchStr, 'pageForView=', pageForView
    print
    'boardList=', boardList, 'count()=', totalCnt
    return render_to_response('service/SearchedPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
                                                            'pageForView': int(pageForView), 'searchStr': searchStr,
                                                            'totalPageList': totalPageList})


def listupdate(request):
    memo_id = request.GET['memo_id']
    current_page = request.GET['current_page']
    searchStr = request.GET['searchStr']
    boardData = Board.objects.get(id=memo_id)
    return render_to_response('service/listUpdate.html', {'memo_id': request.GET['memo_id'],
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
    url = '/searchedPage?searchStr=' + searchStr + '&pageForView=1'
    return HttpResponseRedirect(url)


def authenticate(username, password):
    try:
        user = UserInfo.objects.get(username=username, password=password)
    except ObjectDoesNotExist:
        user = None
    return user


def insert_new_user(username, password):
    user = UserInfo(username=username, password=password)
    user.save()


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
    return render(request, 'service/grade.html')


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


def insert_grade(request):
    if request.method == 'POST':
        userId = request.session['user']
        user = UserInfo.objects.get(username=userId)
        subject = request.POST['_subject']
        grade = request.POST['_grade']
        credit = request.POST['_credit']
        semester = request.POST['_semester']
        if 'true' in request.POST['_major']:
            major = 1
        elif 'false' in request.POST['_major']:
            major = 0

        output = {
            'user': user,
            'subject': subject,
            'grade': grade,
            'credit': credit,
            'semester': semester
        }

        record = Grade(
            user=user, grade=grade, credit=credit, semester=semester, major=major, subject=subject
        )
        record.save()
    return HttpResponseRedirect('/grade')


def grade_calculator(records):
    total_grade = 0
    total_credit = 0

    for record in records:
        credit = record.credit
        grade = record.grade

        val = 0
        if 'A+' in grade:
            val = 4.5
        elif 'A' in grade:
            val = 4
        elif 'B+' in grade:
            val = 3.5
        elif 'B' in grade:
            val = 3
        elif 'C+' in grade:
            val = 2.5
        elif 'C' in grade:
            val = 2
        elif 'D+' in grade:
            val = 1.5
        elif 'D' in grade:
            val = 1
        elif 'P' in grade:
            credit = 0

        total_credit += credit
        total_grade += val * credit
    if total_credit:
        return round(total_grade / total_credit, 2)
    else:
        return 0


def get_total_grade(user):
    return grade_calculator(Grade.objects.filter(user=user))


def get_major_grade(user):
    major_list = Grade.objects.filter(user=user, major=True)

    return grade_calculator(major_list)


def get_not_major_grade(user):
    not_major_list = Grade.objects.filter(user=user, major=False)

    return grade_calculator(not_major_list)


def get_semester_grades(user):
    semester_list = ['1-1', '1-2', '2-1', '2-2', '3-1', '3-2', '4-1', '4-2']

    result = []

    for semester in semester_list:
        semester_grade = Grade.objects.filter(user=user, semester=semester)
        result.append(grade_calculator(semester_grade))

    return result


def get_all_grades(request):
    user = get_current_user(request)

    total = get_total_grade(user)
    major_grade = get_major_grade(user)
    not_major_grade = get_not_major_grade(user)
    semester_grade = get_semester_grades(user)

    return render(request, 'service/grade.html',
                  {'total': total, 'major': major_grade, 'not_major': not_major_grade, 'semester': semester_grade})


def get_current_user(request):
    user_id = request.session['user']
    return UserInfo.objects.get(username=user_id)
