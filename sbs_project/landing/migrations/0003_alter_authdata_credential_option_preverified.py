# Generated by Django 4.2.15 on 2024-10-07 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_authdata_rename_first_userinfo_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authdata',
            name='credential_option_preverified',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
