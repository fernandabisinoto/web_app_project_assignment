from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CreateCustomer(models.Model):
    customerASIN = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        date = timezone.localtime(self.log_date)
        return f"'{self.customerASIN}' logged on {date.strftime('%A, %d %B, %Y at %X')}"