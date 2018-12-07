# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Lib
from .models import FoodA
from .models import FoodB
from .models import FoodC
from .models import Board
from .models import UserInfo
from .models import LoginResult
from .models import LoginRequest

admin.site.register(Lib)
admin.site.register(FoodA)
admin.site.register(FoodB)
admin.site.register(FoodC)
admin.site.register(Board)
admin.site.register(UserInfo)
admin.site.register(LoginResult)
admin.site.register(LoginRequest)
# Register your models here.