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
