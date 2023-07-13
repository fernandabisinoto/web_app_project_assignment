"""
References:
    CreateAccountFormTestCase, RegisterEngineerFormTestCase, and SetTestingStatusFormTestCase based on tests in 'Forms' section and
    ViewsTestCase based on 'Views' section of:

    MDN Contributors (2022) [online] Django Tutorial Part 10. Available at:
    https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing (Accessed: 14 July 2023).

    EngineerTestCase and AccountTestCase were based on the following:

    Django (no date) [online] Writing and running tests | Django documentation. Available at:
    https://docs.djangoproject.com/en/4.0/topics/testing/overview/ (Accessed: 13 July 2023).

    Message response testing based on Stack overflow answer:

    Moppag (2017) [online] python - How can I unit test django messages?, Stack Overflow. Available at:
    https://stackoverflow.com/a/46865530 (Accessed: 11 July 2023).
"""

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.db import connection

from pytz import UTC

from unittest.mock import MagicMock, patch

from web_app.forms import CreateAccountForm, RegisterEngineerForm, SetTestingStatusForm
from web_app.models import Engineer, Account

from authentication_failure_logger import AuthenticationFailureLoggerModelBackend

from middleware.SQLInjectionMiddleware import SQLInjectionMiddleware
from sql_injection_logger import sql_injection_logger


class CreateAccountFormTest(TestCase):
    def setUp(self):
        self.ASIN = "testASIN123"
        self.marketplace = Account.Marketplace.UK
        self.description = "testDescription"
        self.status = Account.Status.A

    def test_empty_form_is_not_valid(self):
        form = CreateAccountForm()

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_ASIN(self):
        form = CreateAccountForm(
            data={"marketplace": self.marketplace, "description": self.description, "status": self.status})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_marketplace(self):
        form = CreateAccountForm(data={"ASIN": self.ASIN, "description": self.description, "status": self.status})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_description(self):
        form = CreateAccountForm(data={"ASIN": self.ASIN, "marketplace": self.marketplace, "status": self.status})

        self.assertFalse(form.is_valid())

    def test_form_is_valid(self):
        form = CreateAccountForm(data={"ASIN": self.ASIN, "marketplace": self.marketplace, "description": self.description, "status": self.status})

        self.assertTrue(form.is_valid())

    def test_form_is_not_valid_if_ASIN_exists(self):
        Engineer.objects.create(name="creator", is_currently_testing=True)
        creator = Engineer.objects.get(name="creator")
        created = timezone.datetime(year=2022, month=1, day=1, tzinfo=UTC)
        Account.objects.create(ASIN="testASIN123",
                               created=created,
                               marketplace=self.marketplace,
                               description=self.description,
                               status=self.status,
                               creator=creator)
        form = CreateAccountForm(
            data={"ASIN": "testASIN123", "marketplace": self.marketplace, "description": self.description, "status": self.status})

        self.assertFalse(form.is_valid())


class RegisterEngineerFormTest(TestCase):
    def setUp(self):
        self.first_name = "testFirstName"
        self.last_name = "testLastName"
        self.username = "testUsername"
        self.email = "test@test.com"
        self.password = "Test_password123"

    def test_empty_form_is_not_valid(self):
        form = RegisterEngineerForm()

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_first_name(self):
        form = RegisterEngineerForm(data={"last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_last_name(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_username(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_email(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "password1": self.password,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_password1(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_password2(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_without_matching_passwords(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": "test_password123",
                                          "is_superuser": False})

        self.assertFalse(form.is_valid())

    def test_form_is_valid_without_is_staff(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": self.password})

        self.assertTrue(form.is_valid())

    def test_form_is_valid(self):
        form = RegisterEngineerForm(data={"first_name": self.first_name,
                                          "last_name": self.last_name,
                                          "username": self.username,
                                          "email": self.email,
                                          "password1": self.password,
                                          "password2": self.password,
                                          "is_superuser": False})

        self.assertTrue(form.is_valid())


class SetTestingStatusFormTest(TestCase):
    def setUp(self):
        Engineer.objects.create(name="test", is_currently_testing=False)

    def test_form_is_not_valid_without_choice(self):
        form = SetTestingStatusForm()

        self.assertFalse(form.is_valid())

    def test_form_is_not_valid_when_choice_is_not_valid(self):
        form = SetTestingStatusForm(data={"engineer": 0})

        self.assertFalse(form.is_valid())

    def test_form_is_valid(self):
        form = SetTestingStatusForm(data={"engineer": 1})

        self.assertTrue(form.is_valid())


class EngineerTest(TestCase):
    def setUp(self):
        Engineer.objects.create(name="firstEngineer", is_currently_testing=True)
        Engineer.objects.create(name="secondEngineer", is_currently_testing=False)

    def test_engineer(self):
        firstEngineer = Engineer.objects.get(name="firstEngineer")
        secondEngineer = Engineer.objects.get(name="secondEngineer")

        self.assertEqual(firstEngineer.__str__(), "firstEngineer")
        self.assertEqual(firstEngineer.is_currently_testing, True)
        self.assertEqual(secondEngineer.__str__(), "secondEngineer")
        self.assertEqual(secondEngineer.is_currently_testing, False)


class AccountTest(TestCase):
    def setUp(self):
        engineer = Engineer.objects.create(name="test_creator", is_currently_testing=True)
        created = timezone.datetime(year=2022, month=1, day=1, tzinfo=UTC)
        Account.objects.create(ASIN="testASIN123",
                               created=created,
                               marketplace=Account.Marketplace.UK,
                               description="description",
                               status=Account.Status.A,
                               creator=engineer)

    def test_account(self):
        account = Account.objects.get(ASIN="testASIN123")

        self.assertEqual(account.ASIN, "testASIN123")
        self.assertEqual(account.created, timezone.datetime(year=2022, month=1, day=1, tzinfo=UTC))
        self.assertEqual(account.marketplace, Account.Marketplace.UK)
        self.assertEqual(account.description, "description")
        self.assertEqual(account.status, Account.Status.A)
        self.assertEqual(account.creator.name, "test_creator")
        self.assertEqual(account.creator.is_currently_testing, True)


class ViewsTest(TestCase):
    def setUp(self):
        self.user_name = "test_user"
        self.user_password = "Test_password123"
        self.admin_name = "test_admin"
        self.admin_password = "Test_admin_password123"
        test_user = User.objects.create_user(username=self.user_name,
                                             email="user@test.com",
                                             password=self.user_password,
                                             first_name="first_name",
                                             last_name="last_name",
                                             is_superuser=False)

        test_admin = User.objects.create_user(username=self.admin_name,
                                              email="admin@test.com",
                                              password=self.admin_password,
                                              first_name="admin_first_name",
                                              last_name="admin_last_name",
                                              is_superuser=True)
        test_user.save()
        test_admin.save()

        engineer = Engineer.objects.create(name="first_name last_name", is_currently_testing=False)
        admin = Engineer.objects.create(name="admin_first_name admin_last_name", is_currently_testing=True)
        created = timezone.datetime(year=2022, month=1, day=1, tzinfo=UTC)
        Account.objects.create(ASIN="testASIN123",
                               created=created,
                               marketplace=Account.Marketplace.UK,
                               description="description",
                               status=Account.Status.A,
                               creator=engineer)

    def test_home_view(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/home.html")

    def test_register_view(self):
        response = self.client.get("/register_eng_form/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/register_eng_form.html")

    def test_register_with_valid_details(self):
        response = self.client.post(reverse("register_eng_form"), data={
            "username": "register",
            "first_name": "regis",
            "last_name": "tering",
            "email": "register@test.com",
            "password1": "Test_password123",
            "password2": "Test_password123",
            "is_superuser": False
        })
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Registration successful.", messages)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 3)

    def test_register_with_invalid_details(self):
        response = self.client.post(reverse("register_eng_form"), data={})
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Unsuccessful registration. Invalid information.", messages)

    def test_login_view(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/login.html")

    def test_login_with_valid_details(self):
        response = self.client.post(reverse("login"), data={
            "username": self.user_name,
            "password": self.user_password
        })
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You are now logged in as test_user.", messages)

    def test_login_with_invalid_details(self):
        response = self.client.post(reverse("login"), data={})
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Invalid username or password.", messages)

    def test_logout(self):
        self.login_helper()
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You have successfully logged out.", messages)

    def test_create_account_view(self):
        response = self.client.get("/create_account_form/")
        self.assertEqual(response.status_code, 302)

        self.login_helper()
        response = self.client.get("/create_account_form/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/create_account_form.html")

    def test_create_account_with_valid_details(self):
        self.login_helper()
        response = self.client.post(reverse("create_account_form"), data={
            "ASIN": "test ASIN",
            "marketplace": "UK",
            "description": "test description",
            "status": "A"
        })
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Account test ASIN has been created.", messages)

    def test_create_account_with_invalid_details(self):
        self.login_helper()
        response = self.client.post(reverse("create_account_form"), data={})
        self.assertEqual(response.status_code, 200)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Form is not valid.", messages)

    def test_set_is_currently_testing_view(self):
        response = self.client.get("/set_testing_status/")
        self.assertEqual(response.status_code, 302)

        self.login_helper()
        response = self.client.get("/set_testing_status/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/set_testing_status.html")

    def test_is_currently_testing(self):
        self.login_helper()
        engineer = Engineer.objects.get(pk=1)
        self.assertFalse(engineer.is_currently_testing)
        response = self.client.post(reverse("set_testing_status"), data={
            "engineer": engineer.pk
        })
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Testing status transferred to first_name last_name.", messages)
        engineer = Engineer.objects.get(pk=1)
        self.assertTrue(engineer.is_currently_testing)

    def test_accounts_view(self):
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 302)

        self.login_helper()
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/accounts.html")

        self.assertTrue("account_list" in response.context)
        self.assertTrue("testing_status" in response.context)

        account_list = response.context["account_list"]
        self.assertEqual(len(account_list), 1)

        account = account_list[0]
        self.assertEqual("testASIN123", account.ASIN)

        testing_status = response.context["testing_status"]
        self.assertEqual(len(testing_status), 1)
        self.assertEqual("admin_first_name admin_last_name", testing_status[0].name)

    def test_user_accounts_view(self):
        response = self.client.get("/user_accounts/")
        self.assertEqual(response.status_code, 302)

        self.login_helper()
        response = self.client.get("/user_accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/user_accounts.html")

    def test_edit_account_view(self):
        self.login_helper()
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)

        account_list = response.context["account_list"]
        account = account_list[0]
        response = self.client.get(reverse("edit_account", args=(account.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/edit_account_form.html")
        self.assertTrue("instance" in response.context)
        instance = response.context["instance"]
        self.assertEqual("testASIN123", instance.ASIN)
        response = self.client.post(reverse("edit_account", args=(account.id,)), data={
            "marketplace": Account.Marketplace.IN,
            "description": "account edited",
            "status": Account.Status.D,

        })
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Account successfully updated.", messages)

        response = self.client.get(reverse("accounts"))
        edited_account_list = response.context["account_list"]
        edited_account = edited_account_list[0]
        self.assertEqual(Account.Marketplace.IN, edited_account.marketplace)
        self.assertEqual("account edited", edited_account.description)
        self.assertEqual(Account.Status.D, edited_account.status)

    def test_delete_account_view(self):
        self.client.post(reverse("login"), data={
            "username": self.admin_name,
            "password": self.admin_password
        })
        response = self.client.get("/accounts/")
        self.assertEqual(response.status_code, 200)

        account_list = response.context["account_list"]
        account = account_list[0]
        response = self.client.get(reverse("delete_account", args=(account.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web_app/delete_account_form.html")
        self.assertTrue("delete_account_form" in response.context)

        response = self.client.post(reverse("delete_account", args=(account.id,)))
        self.assertEqual(response.status_code, 302)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Account successfully deleted.", messages)

        response = self.client.get(reverse("accounts"))
        account_list = response.context["account_list"]
        self.assertEqual(len(account_list), 0)

    """Helper function for login"""
    def login_helper(self):
        self.client.post(reverse("login"), data={
            "username": self.user_name,
            "password": self.user_password
        })


class AuthenticationFailureLoggerModelBackendTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = AuthenticationFailureLoggerModelBackend()
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_authenticate_success(self):
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username=self.username, password=self.password)
        self.assertEqual(user, self.user)

    def test_authenticate_failure(self):
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='invalid', password='password')
        self.assertIsNone(user)
        # Check if the warning log message is generated
        self.assertLogs(logger='authentication_failure_logger.AuthenticationFailureLoggerModelBackend', level='WARNING')


class SQLInjectionMiddlewareTest(TestCase):
    def setUp(self):
        self.get_response = MagicMock()
        self.middleware = SQLInjectionMiddleware(self.get_response)

    def test_sql_injection_warning(self):
        queries = [
            {'sql': 'SELECT * FROM web_app_engineer'},
            {'sql': 'DROP TABLE web_app_engineer'},
        ]

        with patch.object(connection, 'queries', queries):
            self.middleware(None)

        expected_warning = "Potential SQL injection detected: DROP TABLE Engineer"
        self.assertTrue(sql_injection_logger.warning.called)
        self.assertEqual(
            sql_injection_logger.warning.call_args[0][0],
            expected_warning,
        )

    def test_no_sql_injection_warning(self):
        queries = [
            {'sql': 'SELECT * FROM web_app_engineer'},
            {'sql': 'SELECT * FROM web_app_account'},
        ]

        with patch.object(connection, 'queries', queries):
            self.middleware(None)

        self.assertFalse(sql_injection_logger.warning.called)
