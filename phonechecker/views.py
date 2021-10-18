from django.shortcuts import render, redirect
from django.views import generic
from phonechecker.forms import LoginCodeForm, LoginPhoneNumberForm, MySqlForm, UploadForm
from phonechecker.models import *
from phonechecker.serializers import *
from rest_framework import views, generics, response, decorators
from django.core.files.storage import default_storage
from django.utils import timesince, timezone
from uuid import uuid4
from phonechecker import tasks
import os
from django.contrib.auth.decorators import login_required
import urllib.parse


@login_required
def mysql(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = MySqlForm()
        return render(request, 'phonechecker/mysql.html', {"form": form})
    else:
        form = MySqlForm(request.POST)
        if form.is_valid():
            obj = form.save()
            tasks.mysql_import.delay(obj.id)
            tasks.run_telethon.delay(obj.batch_id)
            redirect_url = "{}?{}".format(reverse(
                'tglogin'), urllib.parse.urlencode({'batch_id': obj.batch_id}))
            return redirect(redirect_url)
        else:
            print(form.errors)
            return render(request, 'phonechecker/mysql.html', {"form": form})


@login_required()
def upload(request):
    """
    docstring
    """
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'phonechecker/upload.html', {"form": form})

    if request.method == 'POST':
        form = UploadForm(request.POST, files=request.FILES)
        if form.is_valid():
            # Process here
            obj = form.save()
            tasks.csv_import.delay(obj.id)
            tasks.run_telethon.delay(obj.batch_id)
            redirect_url = "{}?{}".format(reverse(
                'tglogin'), urllib.parse.urlencode({'batch_id': obj.batch_id}))
            return redirect(redirect_url)
        else:
            print(form.errors)
            return render(request, 'phonechecker/upload.html', {"form": form})


def tglogin(request):
    """
    docstring
    """

    if request.method == 'GET':
        batch_id = request.GET.get('batch_id')
        if not batch_id:
            return redirect('upload')

        form1 = LoginPhoneNumberForm(initial={"batch_id": batch_id})
        form2 = LoginCodeForm(initial={"batch_id": batch_id})
        return render(request, 'phonechecker/tglogin.html', {"form1": form1, "form2": form2})
    else:
        form1 = LoginPhoneNumberForm(request.POST)
        form2 = LoginCodeForm(request.POST)
        batch_id = request.POST['batch_id']
        created = False
        if 'submit-phone' in request.POST:
            print("Phone number submitted")
            if form1.is_valid():
                obj, created = BotLogin.objects.update_or_create(batch=batch_id, defaults={
                    "phone_number": form1.cleaned_data['phone_number']
                })
        else:
            print("Code submitted")
            if form2.is_valid():
                obj, created = BotLogin.objects.update_or_create(batch=batch_id, defaults={
                    "code": form2.cleaned_data['code']
                })

        if created:
            return render(request, 'phonechecker/tglogin.html', {"form1": form1, "form2": form2})
        return redirect('/admin/phonechecker/check/')
