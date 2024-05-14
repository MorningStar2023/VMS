from rest_framework import generics, status

from .models import *
from .serializers import *


class Employee_lcv(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class Employee_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class Workshop_lcv(generics.ListCreateAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer


class Workshop_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer


class Zone_lcv(generics.ListCreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class Zone_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class Ward_lcv(generics.ListCreateAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class Ward_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class Route_lcv(generics.ListCreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class Route_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class Vehicle_lcv(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class Vehicle_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class TransferRegister_lcv(generics.ListCreateAPIView):
    queryset = TransferRegister.objects.all()
    serializer_class = TransferRegisterSerializer


class TransferRegister_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransferRegister.objects.all()
    serializer_class = TransferRegisterSerializer


class IncidentLog_lcv(generics.ListCreateAPIView):
    queryset = IncidentLog.objects.all()
    serializer_class = IncidentLogSerializer


class IncidentLog_rud(generics.RetrieveUpdateDestroyAPIView):
    queryset = IncidentLog.objects.all()
    serializer_class = IncidentLogSerializer



