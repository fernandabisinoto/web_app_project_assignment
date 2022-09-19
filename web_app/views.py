import re
from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from web_app.forms import NewCustomerForm, NewEngineerForm
from web_app.models import CreateCustomer
from django.views.generic import ListView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class CustomerListView(ListView):
    login_url = "login"
    model = CreateCustomer

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
    
def new_customer_form(request):
    return render(request, "web_app/new_customer_form.html")   

def new_eng_request(request):
    if request.method == "POST":
        form = NewEngineerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("web_app/home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewEngineerForm()
    return render (request, "web_app/new_eng_form.html", {"register_form":form})    

def create_customer(request):
    form = NewCustomerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            customerASIN = form.save(commit=False)
            customerASIN.log_date = datetime.now()
            customerASIN.save()
            return redirect("home")
    else:
        return render(request, "web_app/log_message.html", {"form": form})    

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			amazon_alias = form.cleaned_data.get('amazon_alias')
			password = form.cleaned_data.get('password')
			user = authenticate(amazon_alias=amazon_alias, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {amazon_alias}.")
				return redirect("web_app/home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "web_app/login.html", {"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("web_app/home")