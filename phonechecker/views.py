from django.shortcuts import render,redirect
from django.views import generic
from phonechecker.forms import TelethonLoginForm
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
