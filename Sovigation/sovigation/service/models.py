# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# 로그인
class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Lib(models.Model):
    libname = models.CharField(max_length=20)
    floor = models.DecimalField(decimal_places=0, max_digits=5)
    room = models.CharField(max_length=20)
    whole = models.DecimalField(decimal_places=0, max_digits=5)
    used = models.DecimalField(decimal_places=0, max_digits=5)
    rest = models.DecimalField(decimal_places=0, max_digits=5)
    updated_at = models.DateTimeField(auto_now=True)


class FoodA(models.Model):
    week = models.CharField(max_length=5)
    prof = models.TextField()
    first = models.TextField()
    special = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class FoodB(models.Model):
    week = models.CharField(max_length=5)
    prof = models.TextField()
    first = models.TextField()
    special = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class FoodC(models.Model):
    week = models.CharField(max_length=5)
    prof = models.TextField()
    first = models.TextField()
    special = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)


class Board(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    created_date = models.DateField(null=True, blank=True)
    mail = models.CharField(max_length=50, blank=True)
    memo = models.CharField(max_length=200, blank=True)
    hits = models.IntegerField(null=True, blank=True)


class LoginRequest(models.Model):
    name = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)


class LoginResult(models.Model):
    name = models.CharField(max_length=50, blank=True)
    result = models.BooleanField()


class Grade(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    credit = models.IntegerField(null=False, default=2)
    semester = models.CharField(max_length=6)
    major = models.BooleanField(null=False, default=False)
    subject = models.CharField(null=True, max_length=20)

# Create your models here.
