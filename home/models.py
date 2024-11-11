from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def get_full_name_department(self):
        return f"{self.name}-{self.department}"
    

class AvailableTime(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    available_date = models.DateField()
    available_time = models.CharField(max_length=20)
    token_count = models.IntegerField()

    class Meta:
        unique_together = ('doctor', 'available_date', 'available_time')

    def __str__(self):
        return str(self.doctor.name) + "|" + str(self.available_date)
    

class PatientToken(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$')
    phone_no = models.CharField(validators=[phone_regex], max_length=10, blank=True, null=True)
    token_no = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('doctor', 'name', 'phone_no', 'date', 'time')

    def __str__(self):
        return self.doctor.name + " | " + self.name



