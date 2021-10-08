from django.shortcuts import render, redirect
from django.views import generic
from phonechecker.forms import TelethonLoginForm, UploadForm
from phonechecker.models import *
from phonechecker.serializers import *
from rest_framework import views, generics, response, decorators
from django.core.files.storage import default_storage
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
        return render(request, 'phonechecker/upload.html', {"form": form})

    if request.method == 'POST':
        batch_id = str(uuid4())
        request.session['batch_id'] = batch_id
        form = UploadForm(request.POST, initial={
                          "batch_id": batch_id}, files=request.FILES)
        if form.is_valid():
            # Process here
            obj = form.save(commit=False)
            obj.batch_id = batch_id
            obj.save()
            tasks.process_upload(batch_id)
            return redirect('tglogin')
        else:
            print(form.errors)
            return render(request, 'phonechecker/upload.html', {"form": form})


def tglogin(request):
    """
    docstring
    """
    batch_id = request.session.get('batch_id')
    if not batch_id:
        return redirect('upload')

    if request.method == 'GET':
        tasks.run_telethon(batch_id)
        form = TelethonLoginForm(initial={"batch_id": batch_id})
        return render(request, 'phonechecker/tglogin.html', {"form": form})
    else:
        form = TelethonLoginForm(data=request.POST)
        if form.is_valid():
            BotLogin.objects.create(
                batch=form.cleaned_data['batch_id'],
                code=form.cleaned_data['code']
            )
            return redirect('/admin/phonechecker/check')
        else:
            return render(request, 'phonechecker/tglogin.html', {"form": form})
