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
from django.views.decorators.csrf import csrf_exempt

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
    result = LoginResult.objects.get(name=ID)
    if result.result:
        url = '/myservice'
    else:
        url = '/login'
    result.delete()
    return HttpResponseRedirect(url)

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
    return render_to_response('service/food.html', {'boardListA': boardListA, 'boardListB': boardListB, 'boardListC': boardListC})


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