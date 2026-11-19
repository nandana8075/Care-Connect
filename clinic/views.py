from django.shortcuts import render, get_object_or_404
from clinic.models import DoctorDb,AppointmentDb
from clinic.serializers import Doctor_Serializer,Appointment_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import time,timedelta,datetime
from rest_framework import serializers

class DoctorListCreateView(APIView):
    def get(self,request):
        qs=DoctorDb.objects.all()
        serializer_instance=Doctor_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=Doctor_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(serializer_instance.errors)

class DoctorRetriveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs=get_object_or_404(DoctorDb,id=pk)
        serialzer_instance=Doctor_Serializer(qs)
        return Response(data=serialzer_instance.data)

    def put(self,request,pk):
        form_data=request.data
        Doctor_object=get_object_or_404(DoctorDb,id=pk)
        serilaizer_instance=Doctor_Serializer(data=form_data,instance=Doctor_object)
        if serilaizer_instance.is_valid():
            serilaizer_instance.save()
            return Response(data=serilaizer_instance.data)
        else:
            return Response (data=serilaizer_instance.errors)

    def delete(self,request,pk):
        DoctorObj=get_object_or_404(DoctorDb,id=pk)
        DoctorObj.delete()
        return Response (data={
                         "messgae":"deleted successfully"})


class AppointmentListCreateView(APIView):
    def get(self,request):
        qs=AppointmentDb.objects.all()
        serializer_instance=Appointment_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=Appointment_Serializer(data=form_data)
        if serializer_instance.is_valid():
            print(serializer_instance.validated_data)
            appointment_date=serializer_instance.validated_data.get("appointment_date")
            doctor_id=serializer_instance.validated_data.get("doctor_id")
            last_appointment=AppointmentDb.objects.filter(appointment_date=appointment_date,doctor_id=doctor_id).order_by("-token_number").first()
            if last_appointment is None:
                form_data["token_number"]=1
                form_data["appointment_time"]=time(10,0)


            else:
                next_token=last_appointment.token_number+1
                current_time= datetime.combine(appointment_date,last_appointment.appointment_time)
                next_time=current_time+timedelta(minutes=15)
                
                #adding lunch break
                if next_time.time()==time(12,00):
                    next_time=datetime.combine(appointment_date,time(13,30))

                #adding slot completion
                if next_time.time()==time(17,00):
                    raise serializers.ValidationError("NO SLOT TODAY")

                form_data["token_number"]=next_token
                form_data["appointment_time"]=next_time.time()

            qs=AppointmentDb.objects.create(**form_data)
            serializer_instance=Appointment_Serializer(qs)
            return Response(data={
                "message":"booked successfully..!",
                "token number is": form_data["token_number"]
            })
        else:
            return Response(data=serializer_instance.errors)





