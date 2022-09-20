import re
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from web_app.forms import NewCustomerForm, NewEngineerForm
from web_app.models import Customers
from django.views.generic import ListView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

class CustomerListView(ListView):
    login_url = "login"
    model = Customers

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        return context

def hello_there(request, name):
    return render(
        request,
        'web_app/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home_request(request):
    return render(request, "web_app/home.html")

def device(request):
    return render(request, "web_app/device.html")

def create_eng(request):
    form = NewEngineerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render (request, "web_app/new_eng_form.html", {"register_form":form})    

@login_required(login_url="login")
def create_customer(request):
    form = NewCustomerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            customerASIN = form.save(commit=False)
            customerASIN.log_date = datetime.now()
            customerASIN.save()
            return redirect("customers")
    else:
        return render(request, "web_app/new_customer_form.html", {"form": form})    

def login_request(request):
    form = AuthenticationForm(request, data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("customers")
        messages.error(request,"Invalid username or password.")
    return render(request, "web_app/login.html", {"login_form":form})

@login_required(login_url="login")
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")