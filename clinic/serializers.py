from rest_framework import serializers
from clinic.models import DoctorDb,AppointmentDb
from django.utils import timezone
class Doctor_Serializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorDb
        fields = "__all__"
        read_only_fields=["id"]

class Appointment_Serializer(serializers.ModelSerializer):
    class Meta:
        model=AppointmentDb
        fields="__all__"
        read_only_fields=["id"]

    def validate(self,validated_data):
        phone=validated_data.get("phone")
        appointment_date=validated_data.get("appointment_date")
        if appointment_date<timezone.localdate():
            raise serializers.ValidationError("Invalid date")
        if AppointmentDb.objects.filter(phone=phone,appointment_date=appointment_date).exists():
            raise serializers.ValidationError("already booked..!")
        else:
            return validated_data

    

