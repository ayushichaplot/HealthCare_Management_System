from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Patient, Visit
from .serializers import PatientSerializer, VisitGetSerializer, VisitPostSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_patient(request, pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single patient
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    # delete a single patient
    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # update details of a single patient
    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_patients(request):
    # get all patient
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
        return Response({})
    # insert a new record for a patient
    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_visits(request):
    if request.method == 'GET':
        visits = Visit.objects.all()
        visit_serializer = VisitGetSerializer(visits, many=True)
        return Response(visit_serializer.data)
        return Response({})
        # insert a new record for a patient
    elif request.method == 'POST':
        serializer = VisitPostSerializer(data=request.data)
        if serializer.is_valid():
            visit = serializer.save()
            serializer = VisitPostSerializer(visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_visit(request, pk):
    try:
        visit = Visit.objects.get(pk=pk)
    except Visit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single visit
    if request.method == 'GET':
        serializer = VisitGetSerializer(visit)
        return Response(serializer.data)

    # delete a single visit
    elif request.method == 'DELETE':
        visit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # update details of a single visit
    elif request.method == 'PUT':
        serializer = VisitPostSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
