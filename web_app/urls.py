from django.urls import path
from web_app import views
from web_app.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="web_app/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),
    path("web_app/<name>", views.hello_there, name="hello_there"),
    path("customer/", views.customer, name="customer"),
    path("device/", views.device, name="device"),
    path("new_customer_form/", views.new_customer_form, name="new_customer_form"),
    path("login/", views.login, name="login"),
    path("new_eng_form/", views.new_eng_form, name="new_eng_form"),
    path("logout/", views.log_message, name="logout"),
]