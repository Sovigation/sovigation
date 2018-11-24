# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db import models


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


# Create your models here.
