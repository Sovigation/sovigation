# Create your views here.
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import Lib
from .models import FoodA
from .models import FoodB
from .models import FoodC
from .models import UserInfo
from django.core.exceptions import ObjectDoesNotExist

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


def lib(request):
    boardList = Lib.objects.order_by('-id')[0:5]
    return render_to_response('lib.html', {'boardList': boardList})


def fooda(request):
    boardList = FoodA.objects.order_by('-id')[0:6]
    return render_to_response('foodaPage.html', {'boardList': boardList})


def foodb(request):
    boardList = FoodB.objects.order_by('-id')[0:6]
    return render_to_response('foodbPage.html', {'boardList': boardList})


def foodc(request):
    boardList = FoodC.objects.order_by('-id')[0:6]
    return render_to_response('foodcPage.html', {'boardList': boardList})


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username, password)

        if user is None:
            insert_new_user(username, password)
            return myService(request)
        else:
            return myService(request)
        # if user is not None:
        #     login(request, user)
        #     return redirect('index')
        # else:
        #     return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        return login(request)


def authenticate(username, password):
    try:
        user = UserInfo.objects.get(username=username, password=password)
    except ObjectDoesNotExist:
        user = None
    return user


def insert_new_user(username, password):
    user = UserInfo(username=username, password=password)
    user.save()
