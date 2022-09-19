from django.urls import path
from web_app import views
from web_app.models import CreateCustomer

customer_list_view = views.CustomerListView.as_view(
    queryset=CreateCustomer.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="customer_list",
    template_name="web_app/customer.html",
)

urlpatterns = [
    path("web_app/<name>", views.hello_there, name="hello_there"),
    path("", views.home_request, name="home"),
    path("customer/", customer_list_view, name="customer"),
    path("device/", views.device, name="device"),
    path("new_customer_form/", views.new_customer_form, name="new_customer_form"),
    path("new_eng_form/", views.new_eng_request, name="new_eng_form"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]