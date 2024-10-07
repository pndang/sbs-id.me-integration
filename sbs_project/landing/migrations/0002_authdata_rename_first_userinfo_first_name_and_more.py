# Generated by Django 4.2.13 on 2024-10-07 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aud', models.CharField(max_length=255, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('credential_option_preverified', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('exp', models.DateTimeField(blank=True, null=True)),
                ('fname', models.CharField(max_length=255, null=True)),
                ('iat', models.DateTimeField(blank=True, null=True)),
                ('identifier', models.CharField(max_length=255, null=True)),
                ('iss', models.CharField(max_length=255, null=True)),
                ('lname', models.CharField(max_length=255, null=True)),
                ('phonels', models.CharField(blank=True, max_length=20, null=True)),
                ('sub', models.CharField(max_length=255, null=True)),
                ('transaction', models.CharField(max_length=255, null=True)),
                ('uuid', models.CharField(max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='first',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='last',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='userinfo',
            old_name='travelerClass',
            new_name='traveler_class',
        ),
    ]