import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from web_app.forms import LogMessageForm
from web_app.models import LogMessage
from django.views.generic import ListView

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "web_app/about.html")

def contact(request):
    return render(request, "web_app/contact.html")

def hello_there(request, name):
    return render(
        request,
        'web_app/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "web_app/log_message.html", {"form": form})    