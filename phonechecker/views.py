from django.shortcuts import render, redirect
from django.views import generic
from phonechecker.forms import TelethonLoginForm, UploadForm
from phonechecker.models import *
from phonechecker.serializers import *
from rest_framework import views, generics, response, decorators
from django.utils import timesince, timezone
from uuid import uuid4
from phonechecker import tasks
import os


def upload(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'phonechecker/upload.htm', {"form": form})

    if request.method == 'POST':
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # Process here
            return redirect("")


def tglogin(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = TelethonLoginForm()
        return render(request, 'phonechecker/tglogin.html', {"form": form})
    else:
        form = TelethonLoginForm(data=request.POST)
        if form.is_valid():
            # porcess here
            return redirect("")
        else:
            return render(request, 'phonechecker/tglogin.html', {"form": form})
