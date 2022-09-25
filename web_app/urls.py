from django.urls import path
from django.conf.urls import url

from web_app import views

account_list_view = views.AccountListView.as_view(template_name="web_app/accounts.html")
user_account_list_view = views.AccountListView.as_view(template_name="web_app/user_accounts.html")
delete_account_list_view = views.AccountDeleteView.as_view(template_name="web_app/delete_account_form.html")

urlpatterns = [
    url(r'^accounts/update/(?P<pk>\d)/$', views.edit_account_request, name="edit_account"),
    url(r'^accounts/delete/(?P<pk>\d)/$', delete_account_list_view, name="delete_account"),
    path("", views.home_request, name="home"),
    path("accounts/", account_list_view, name="accounts"),
    path("user_accounts/", user_account_list_view, name="user_accounts"),
    path("set_testing_status/", views.set_testing_status_request, name="set_testing_status"),
    path("create_account_form/", views.create_account_request, name="create_account_form"),
    path("register_eng_form/", views.register_eng_request, name="register_eng_form"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]