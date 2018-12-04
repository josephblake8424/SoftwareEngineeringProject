from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.template import loader
from .models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from django_datatables_view.base_datatable_view import BaseDatatableView
# Create your views here.
"""
def index(request):
    return HttpResponse("Welcome to HPE File Browser 0.0.1")
"""

class dtSystems(BaseDatatableView):
	model = System
	columns = ["serialNumberInserv", "name", "tenants"]
	order_columns = ["serialNumberInserv", "name", "tenants"]

def systems(request):
    return render(request, 'browser/systems_page.html')
    if not request.session.has_key('username'):
        return redirect("browser:login")
    username = request.session['username']
    return render(request)


def files(request, serialNumberInserv):
    if not request.session.has_key('username'):
        return redirect("browser:login")
    files = get_list_or_404(File, SystemID = serialNumberInserv)
    system = get_object_or_404(System, serialNumberInserv=serialNumberInserv)
    return render(request, 'browser/files_page.html', {'file_list':files, 'companyID':serialNumberInserv, 
        'companyName':system.name})


def help(request):
    if not request.session.has_key('username'):
        return redirect("browser:login")
    return render(request, 'browser/help.html', {})

def loginView(request):
    errors = []
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            usr = login_form.cleaned_data['username']
            pswd = login_form.cleaned_data['password']
            try:
                u = customUser.objects.get(username=usr)
                if check_password(pswd, u.password):
                    request.session['username'] = usr
                    return redirect("browser:systems")
                else:
                    errors = ['invalid password']
            except ObjectDoesNotExist:
                errors = ['invalid username']
        else:
            errors = ['invalid username or password']

    return render(request, 'browser/login.html', {'error' : errors})

def logoutView(request):
    try:
      del request.session['username']
    except:
      pass
    return redirect("browser:login")
