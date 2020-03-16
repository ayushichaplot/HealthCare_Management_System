from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Patient (models.Model):

    pfname = models.CharField(max_length=100, default='Enter First Name')
    plname = models.CharField(max_length=100, default='Enter Last Name')
    paddress = models.CharField(max_length=100, default='Enter Address')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Between 10-15 digits allowed.")
    pphone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, default='Enter number')

    def __str__(self):
        return self.pfname

class Visit(models.Model):

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    visit_start_date = models.DateField()
    visit_end_date = models.DateField()

    def clean(self):
        if self.visit_end_date < self.visit_start_date:
            raise ValidationError("End date must be after start date.")

    def __str__(self):
        return "visit" + str(self.id)



