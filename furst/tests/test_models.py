from django.core.exceptions import ValidationError
from django.test import TestCase
from ..models import Patient,Visit
import datetime

# Create your tests here.
class PatientTestCase(TestCase):
    def setUp(self):
        Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur', pphone_number='1234000000')
        Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai', pphone_number=1234567899)


    def test_patient_info(self):
        patient = Patient.objects.all()
        self.assertEqual(patient.count(),2)
        p1 = Patient.objects.get(pfname='Jerry')
        p2 = Patient.objects.get(pfname='Tom')
        self.assertEqual(p1.paddress, 'Udaipur')
        self.assertEqual(p2.paddress, 'Mumbai')

    def test_first_name_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pfname').max_length
        self.assertEquals(max_length, 100)

    def test_phonenumber(self):
        phone_number = Patient(pphone_number='1234567as')
        with self.assertRaises(ValidationError):
            phone_number.full_clean()


'''
    def test_phonenumber(self):
        phone_number = Patient(pphone_number = '1234567890')
        with self.assertRaisesRegex(ValidationError, expected_regex=r'^\+?1?\d{10,15}$'):
            phone_number.full_clean()

'''



class VisitTestCase(TestCase):
    def setUp(self):
        user1 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur', pphone_number='1234000000')
        user2 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai', pphone_number=1234567899)

        Visit.objects.create(patient=user1,visit_start_date=datetime.date(2020,3,3), visit_end_date=datetime.date(2020,3,5))
        Visit.objects.create(patient=user2,visit_start_date=datetime.date(2020,2,3), visit_end_date=datetime.date(2020,2,2))

    def test_fields_visit(self):
        record = Visit.objects.get(id=1)
        self.assertEqual(record.patient.pfname, 'Jerry')
        visit = Visit.objects.all()
        self.assertEqual(visit.count(),2)

    def test_validation(self):
        #date = Visit(visit_start_date=datetime.date(2020,3,3), visit_end_date=datetime.date(2020,3,5))
        date = Visit.objects.get(id=2)
        date.save()
        with self.assertRaises(ValidationError):
            date.full_clean()






