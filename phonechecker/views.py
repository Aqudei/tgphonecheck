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
from django.core.files.storage import default_storage


def upload(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'phonechecker/upload.html', {"form": form})

    if request.method == 'POST':
        batch_id = str(uuid4())
        form = UploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # Process here
            file = form.cleaned_data['file']
            with default_storage.open("tmp/numbers.csv", 'wb') as outfile:
                for chunk in file.chunks():
                    outfile.write(chunk)
                tasks.process_upload(batch_id)
                return redirect('/checker/tglogin/{}'.format(batch_id))
        else:
            return render(request, 'phonechecker/upload.html', {"form": form})


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
