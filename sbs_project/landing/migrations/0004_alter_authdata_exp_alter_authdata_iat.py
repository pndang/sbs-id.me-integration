# Generated by Django 4.2.15 on 2024-10-20 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_alter_authdata_credential_option_preverified'),
    ]

    operations = [
        ## DID NOT WORK
        # migrations.AlterField(
        #     model_name='authdata',
        #     name='exp',
        #     field=models.IntegerField(blank=True, null=True),
        # ),
        # migrations.AlterField(
        #     model_name='authdata',
        #     name='iat',
        #     field=models.IntegerField(blank=True, null=True),
        # ),

        # Remove
        migrations.RemoveField(
            model_name='authdata',
            name='exp',
        ),
        migrations.RemoveField(
            model_name='authdata',
            name='iat',
        ),

        # Add back
        migrations.AddField(
            model_name='authdata',
            name='exp',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='authdata',
            name='iat',
            field=models.BigIntegerField(blank=True, null=True),
        ),

        # migrations.AlterField(
        #     model_name='authdata',
        #     name='exp',
        #     field=models.BigIntegerField(null=True, blank=True),
        #     ),
        # migrations.AlterField(
        #     model_name='authdata',
        #     name='iat',
        #     field=models.BigIntegerField(null=True, blank=True),
        #     ),
    ]
