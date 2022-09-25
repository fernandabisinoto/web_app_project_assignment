"""
References:
    TicketListView based on 'HomeListView', create_ticket_request and set_on_call_request based on 'log_message'
    in 'use the database through the models' section of Django tutorial:

    Visual Studio Code (no date) [online] Python and Django tutorial in Visual Studio Code. Available at:
    https://code.visualstudio.com/docs/python/tutorial-django (Accessed: 07 September 2022).

    TicketDeleteView based on 'DeleteView' in Django documentation:

    Django (no date) [online] Generic editing views | Django documentation. Available at:
    https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView
    (Accessed: 09 September 2022).

    register_request and login_request based on 'add register/login functions to views' sections of:

    Ordinary Coders (2020) [online] A Guide to User Registration, Login, and Logout in Django. Available at:
    https://ordinarycoders.com/blog/article/django-user-register-login-logout (Accessed: 15 September 2022).

    edit_ticket_request based on Stack overflow comment:

    Roseman, D. (2018) [online] Django, how to include pre-existing data in update form view, Stack Overflow.
    Available at: https://stackoverflow.com/a/52494854 (Accessed: 15 September 2022).
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView
from django.contrib.auth import login, authenticate, get_user, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone

from web_app.forms import CreateAccountForm, RegisterEngineerForm, EditAccountForm, SetTestingStatusForm
from web_app.models import Account, Engineer

class AccountListView(LoginRequiredMixin, ListView):
    login_url = "login"
    model = Account
    context_object_name = "account_list"

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        context["testing_status"] = Engineer.objects.filter(is_currently_testing=True)
        return context

    def get_queryset(self):
        if self.request.path == "/user_accounts/":
            user = get_user(self.request)
            return Account.objects.filter(creator__name=user.get_full_name()) 
        return Account.objects.all()


class AccountDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "user.is_superuser"
    model = Account
    context_object_name = "delete_account_form"

    def get_success_url(self):
        messages.info(self.request, "Account successfully deleted.")
        return reverse_lazy("accounts")

def home_request(request):
    return render(request, "web_app/home.html")

@login_required(login_url="login")
def create_account_request(request):
    form = CreateAccountForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            account = form.save(commit=False)
            account.created = timezone.now()
            user = get_user(request)
            creator = Engineer.objects.filter(name=user.get_full_name())
            if creator.count() != 0:
                account.creator = creator[0]
            account.save()
            messages.info(request, f"Account {account.ASIN} has been created.")
            return redirect("accounts")
        messages.error(request, "Form is not valid.")
    return render(request, "web_app/create_account_form.html", {"create_account_form": form})

@login_required(login_url="login")
def edit_account_request(request, pk):
    try:
        instance = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        instance = None
        messages.error(request, "Account does not exist.")
    form = EditAccountForm(data=request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.info(request, "Account successfully updated.")
            return redirect("accounts")
        messages.error(request, "Form is not valid.")
    return render(request=request, template_name="web_app/edit_account_form.html",
                  context={"edit_account_form": form, "instance": instance})    

def register_eng_request(request):
    form = RegisterEngineerForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render (request, "web_app/register_eng_form.html", {"register_eng_form":form})    

def login_request(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("accounts")
        messages.error(request,"Invalid username or password.")
    return render(request, "web_app/login.html", {"login_form":form})

@login_required(login_url="login")
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

@login_required(login_url="login")
def set_testing_status_request(request):
    form = SetTestingStatusForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            engineer_id = form.cleaned_data.get("engineer").id
            Engineer.objects.filter(is_currently_testing=True).update(is_currently_testing=False)
            engineer = Engineer.objects.get(pk=engineer_id)
            engineer.is_currently_testing = True
            engineer.save(update_fields=["is_currently_testing"])
            messages.info(request, f"Testing status transferred to {engineer.name}.")
            return redirect("accounts")
    return render(request, "web_app/set_testing_status.html", {"set_testing_status": form})