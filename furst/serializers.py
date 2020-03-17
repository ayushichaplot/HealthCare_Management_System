from rest_framework import serializers
from .models import Patient, Visit


class PatientSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    class Meta:
        model = Patient
        fields = '__all__'


class VisitGetSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()

    class Meta:
        model = Visit
        fields = '__all__'


class VisitPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient'] = PatientSerializer(instance.patient).data
        return response

    def validate(self, data):
        if data['visit_end_date'] < data['visit_start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


'''
    def create(self, validated_data):
        patient_validated_data = validated_data.pop('patient')
        visit = Visit.objects.create(**validated_data)
        patient_set_serializer = self.fields['patient']
        for each in patient_validated_data:
            each['visit'] = visit
        patients = patient_set_serializer.create(patient_validated_data)
        return visit
        '''
''''
    def create(self, validated_data):
        patient = validated_data.pop('patient')
        visit = Visit.objects.create(**validated_data)
        Patient.objects.create(**patient, visit=visit)
        return visit
        '''

'''
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(ProfileSerializer, self).to_representation(instance)
'''
