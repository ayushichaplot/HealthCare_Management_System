from django.core.exceptions import ValidationError
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.test import TestCase
from ..models import Patient, Visit
from ..serializers import PatientSerializer, VisitPostSerializer, VisitGetSerializer

client = Client()


class GetAllPatientsTest(TestCase):
    """ Test module for GET all patients API """

    def setUp(self):
        Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur', pphone_number=123456712)
        Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai', pphone_number=12345671211)
        Patient.objects.create(pfname='Doraemon', plname='sharma', paddress='Hyd', pphone_number=1234567121)
        Patient.objects.create(pfname='Nobita', plname='sharma', paddress='Banglore', pphone_number=12345671112)

    def test_get_all_patients(self):
        # get API response from urls.py
        response = client.get(reverse('get_post_patients'))
        # get data from db
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePatientTest(TestCase):
    """ Test module for GET single patient API """

    def setUp(self):
        self.patient1 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur',
                                               pphone_number=123456712)
        self.patient2 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai',
                                               pphone_number=12345671211)
        self.patient3 = Patient.objects.create(pfname='Doraemon', plname='sharma', paddress='Hyd',
                                               pphone_number=1234567121)
        self.patient4 = Patient.objects.create(pfname='Nobita', plname='sharma', paddress='Banglore',
                                               pphone_number=12345671112)

    def test_get_valid_single_patient(self):
        response = client.get(reverse('get_delete_update_patient', kwargs={'pk': self.patient1.pk}))
        patient = Patient.objects.get(pk=self.patient1.pk)
        serializer = PatientSerializer(patient)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_patient(self):
        response = client.get(reverse('get_delete_update_patient', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPatientTest(TestCase):
    """ Test module for inserting a new patient """

    def setUp(self):
        self.valid_payload = {

            'pfname': 'Jerry',
            'plname': 'Jain',
            'paddress': 'Udaipur',
            'pphone_number': '1234567890',
        }
        self.invalid_payload = {

            'pfname': '',
            'plname': '',
            'paddress': '',
            'pphone_number': '12345as',
        }

    def test_create_valid_patient(self):
        response = client.post(reverse('get_post_patients'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_paient(self):
        response = client.post(reverse('get_post_patients'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePatientTest(TestCase):
    """ Test module for updating an existing patient record """

    def setUp(self):
        self.patient1 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur',
                                               pphone_number=123456712)
        self.patient2 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai',
                                               pphone_number=12345671211)

        self.valid_payload = {

            'pfname': 'Jerry',
            'plname': 'sharma',
            'paddress': 'Delhi',
            'pphone_number': '1234567891',
        }
        self.invalid_payload = {

            'pfname': '',
            'plname': 'sharma',
            'paddress': '',
            'pphone_number': '123as',
        }

    def test_valid_update_patient(self):
        response = client.put(
            reverse('get_delete_update_patient', kwargs={'pk': self.patient1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_patient(self):
        response = client.put(
            reverse('get_delete_update_patient', kwargs={'pk': self.patient1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePatientTest(TestCase):
    """ Test module for deleting an existing patient record """

    def setUp(self):
        self.patient1 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Udaipur',
                                               pphone_number=123456712)
        self.patient2 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Mumbai',
                                               pphone_number=12345671211)

    def test_valid_delete_patient(self):
        response = client.delete(
            reverse('get_delete_update_patient', kwargs={'pk': self.patient1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_patient(self):
        response = client.delete(
            reverse('get_delete_update_patient', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllVisitsTest(TestCase):
    """ Test module for GET all patients API """

    def setUp(self):
        patient1 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Udaipur', pphone_number=8385925886)
        patient2 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Mumbai', pphone_number=8078603966)
        patient3 = Patient.objects.create(pfname='Doraemon', plname='Jain', paddress='Pune', pphone_number=9461201494)
        Visit.objects.create(patient=patient1, visit_start_date="2020-01-03", visit_end_date="2020-02-02")
        Visit.objects.create(patient=patient2, visit_start_date="2020-02-03", visit_end_date="2020-02-05")
        Visit.objects.create(patient=patient3, visit_start_date="2020-01-10", visit_end_date="2020-02-05")

    def test_get_all_visits(self):
        # get API response from urls.py
        response = client.get(reverse('get_post_visits'))
        # get data from db
        visits = Visit.objects.all()
        serializer = VisitGetSerializer(visits, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleVisitTest(TestCase):
    """ Test module for GET single visit API """

    def setUp(self):
        patient1 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Udaipur', pphone_number=8385925886)
        self.visit1 = Visit.objects.create(patient=patient1, visit_start_date="2020-01-03", visit_end_date="2020-02-02")

    def test_get_valid_single_visit(self):
        response = client.get(reverse('get_delete_update_visit', kwargs={'pk': self.visit1.pk}))
        visit = Visit.objects.get(pk=self.visit1.pk)
        serializer = VisitGetSerializer(visit)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_visit(self):
        response = client.get(reverse('get_delete_update_visit', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewVisitTest(TestCase):
    """ Test module for inserting a new visit """

    def setUp(self):
        patient1 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Udaipur', pphone_number=8385925886)
        self.valid_payload = {
            'patient': patient1.id,
            'visit_start_date': "2020-03-03",
            'visit_end_date': "2020-03-05"

        }
        self.invalid_payload = {
            'patient': '',
            'visit_start_date': '2020-03-03',
            'visit_end_date': '2020-03-02',
        }

    def test_create_valid_visit(self):
        response = client.post(reverse('get_post_visits'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_visit(self):
        response = client.post(reverse('get_post_visits'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json'
                               )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleVisitTest(TestCase):
    """ Test module for updating an existing visit record """

    def setUp(self):
        patient1 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Udaipur', pphone_number=8385925886)
        self.visit1 = Visit.objects.create(patient=patient1, visit_start_date="2020-01-03", visit_end_date="2020-02-02")
        patient2 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Pune', pphone_number=8078603966)
        self.visit2 = Visit.objects.create(patient=patient2, visit_start_date="2020-02-03", visit_end_date="2020-03-02")

        self.valid_payload = {
            'patient': patient2.id,
            'visit_start_date': "2020-01-03",
            'visit_end_date': "2020-03-05"

        }
        self.invalid_payload = {
            'patient': '',
            'visit_start_date': '2020-03-03',
            'visit_end_date': '2020-03-02',
        }

    def test_valid_update_visit(self):
        response = client.put(
            reverse('get_delete_update_visit', kwargs={'pk': self.visit1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_visit(self):
        response = client.put(
            reverse('get_delete_update_visit', kwargs={'pk': self.visit1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleVisitTest(TestCase):
    """ Test module for deleting an existing visit record """

    def setUp(self):
        patient1 = Patient.objects.create(pfname='Tom', plname='Jain', paddress='Udaipur', pphone_number=8385925886)
        self.visit1 = Visit.objects.create(patient=patient1, visit_start_date="2020-01-03", visit_end_date="2020-02-02")
        patient2 = Patient.objects.create(pfname='Jerry', plname='Jain', paddress='Pune', pphone_number=8078603966)
        self.visit2 = Visit.objects.create(patient=patient2, visit_start_date="2020-02-03", visit_end_date="2020-03-02")

    def test_valid_delete_visit(self):
        response = client.delete(
            reverse('get_delete_update_visit', kwargs={'pk': self.visit1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_visit(self):
        response = client.delete(
            reverse('get_delete_update_visit', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
