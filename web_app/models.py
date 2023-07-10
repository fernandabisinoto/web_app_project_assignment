"""
References:
    Engineer and Account models were based on the code in the 'define models' section of Django tutorial:

    Visual Studio Code (no date) [online] Python and Django tutorial in Visual Studio Code. Available at:
    https://code.visualstudio.com/docs/python/tutorial-django (Accessed: 13 July 2023).
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Engineer(models.Model):
    is_currently_testing = models.BooleanField(
        _('testing status'),
        default=False,
        help_text=_(
            'States if engineer is currently testing'
        ),
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Account(models.Model):
    class Marketplace(models.TextChoices):
        US = 'US', 'United States'
        UK = 'UK', 'United Kingdom'
        IN = 'IN', 'India'

    class Status(models.TextChoices):
        A = 'A', 'Active'
        IU = 'IU', 'In use'
        D = 'D', 'Deactivated'

    ASIN = models.CharField(
        _('account ASIN'),
        help_text=_(
            'Account ASIN (Amazon Standard Identification Number)'
        ),
        max_length=50,
        unique=True,
    )

    created = models.DateTimeField('date created')

    marketplace = models.CharField(
        _('account marketplace'),
        choices=Marketplace.choices,
        default=Marketplace.UK,
        help_text=_(
            'Describes the marketplace in which the account will be used. UK = United Kingdom, US = United States, IN = India'
        ),
        max_length=50
    ) 

    description = models.CharField(
        _('account description'),
        default='',
        help_text=_(
            'Describes the reason for account creation, such as "Test Contextual functions in the US"'
        ),
        max_length=300
    )

    status = models.CharField(
        _('account status'),
        choices=Status.choices,
        default=Status.A,
        help_text=_(
            'Describes the current state of the account. A = Active do, IS = In use, D = Deactivated'
        ),
        max_length=50
    )

    creator = models.ForeignKey(Engineer, on_delete=models.CASCADE, blank=True)