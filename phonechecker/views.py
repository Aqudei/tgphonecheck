from django.shortcuts import render, redirect
from django.views import generic
from phonechecker.forms import TelethonLoginForm
from phonechecker.models import *
from phonechecker.serializers import *
from rest_framework import views, generics, response
from django.utils import timesince, timezone
from uuid import uuid4

# Create your views here.


def tglogin(request):
    if request.method == "GET":
        form = TelethonLoginForm()
        return render(request, "phonechecker/tglogin.html", {"login_form": form})
    else:
        form = TelethonLoginForm(data=request.POST)
        if not form.is_valid():
            return render(request, "phonechecker/base.html", {"login_form": form})

    return redirect('tglogin')


class CheckView(views.APIView):
    """
    docstring
    """

    def post(self, request):
        """
        docstring
        """
        _uuid = str(uuid4())
        checks = [Check(phone_number=phone, batch=_uuid)
                  for phone in PhoneNumber.objects.all()]
        Check.objects.bulk_create(checks)
        serializer = CheckSerializer(
            Check.objects.filter(batch=_uuid), many=True)
        return response.Response(serializer.data)

    def patch(self, request, pk=None):
        """
        docstring
        """
        if not pk:
            return
        result = request.data['result']
        obj = Check.objects.get(pk=pk)
        obj.timestamp = timezone.now()
        obj.result = result
        obj.save()
        return response.Response()
