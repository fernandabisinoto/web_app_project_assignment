from django.urls import path
from web_app import views
from web_app.models import Customers

customer_list_view = views.CustomerListView.as_view(
    queryset=Customers.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="customer_list",
    template_name="web_app/customer.html",
)

urlpatterns = [
    path("web_app/<name>", views.hello_there, name="hello_there"),
    path("", views.home_request, name="home"),
    path("customers/", customer_list_view, name="customers"),
    path("device/", views.device, name="device"),
    path("new_customer_form/", views.create_customer, name="new_customer_form"),
    path("new_eng_form/", views.create_eng, name="new_eng_form"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]