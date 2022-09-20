from unicodedata import name
from django.db import models
from django.utils import timezone

# class Engineers(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

class Customers(models.Model):
    customerASIN = models.CharField(max_length=100)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        date = timezone.localtime(self.log_date)
        return f"'{self.customerASIN}' logged on {date.strftime('%A, %d %B, %Y at %X')}"