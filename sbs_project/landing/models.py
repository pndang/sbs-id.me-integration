from django.db import models

# Create your models here.

class UserInfo(models.Model):
    travelerClassChoices = [
        ('GEP', 'Global Entry PLUS'),
        ('SP', 'Sentri PLUS'),
        ('RLP', 'Ready Lane PLUS'),
        ('ATP', 'All traffic PLUS'),
        ('ESTA', 'ESTA'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    traveler_class = models.CharField(max_length=4, choices=travelerClassChoices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.traveler_class}"

class AuthData(models.Model):
    aud = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True, blank=True)
    credential_option_preverified = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True, blank=True)
    exp = models.DateTimeField(null=True, blank=True)
    fname = models.CharField(max_length=255, null=True)
    iat = models.DateTimeField(null=True, blank=True)
    identifier = models.CharField(max_length=255, null=True)
    iss = models.CharField(max_length=255, null=True)
    lname = models.CharField(max_length=255, null=True)
    phonels = models.CharField(max_length=20, null=True, blank=True)
    sub = models.CharField(max_length=255, null=True)
    transaction = models.CharField(max_length=255, null=True)
    uuid = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.fname} {self.lname} - {self.timestamp}'