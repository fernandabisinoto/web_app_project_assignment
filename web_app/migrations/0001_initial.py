from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_currently_testing', models.BooleanField(default=False, help_text='States if engineer is currently testing', verbose_name='testing status')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ASIN', models.CharField(help_text='Account ASIN (Amazon Standard Identification Number)', max_length=50, unique=True, verbose_name='account ASIN')),
                ('created', models.DateTimeField(verbose_name='date created')),
                ('marketplace', models.CharField(choices=[('US', 'United States'), ('UK', 'United Kingdom'), ('IN', 'India')], default='UK', help_text='Describes the marketplace in which the account will be used. UK = United Kingdom, US = United States, IN = India', max_length=50, verbose_name='account marketplace')),
                ('description', models.CharField(default='', help_text='Describes the reason for account creation, such as "Test Contextual functions in the US"', max_length=300, verbose_name='account description')),
                ('status', models.CharField(choices=[('A', 'Active'), ('IU', 'In use'), ('D', 'Deactivated')], default='A', help_text='Describes the current state of the account. A = Active do, IS = In use, D = Deactivated', max_length=50, verbose_name='account status')),
                ('creator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='web_app.engineer')),
            ],
        ),
    ]
