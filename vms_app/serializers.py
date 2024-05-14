from rest_framework import serializers

from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class TransferRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferRegister
        fields = '__all__'


class IncidentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentLog
        fields = '__all__'


class TripHistorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = TripHistory
        fields = '__all__'


# Testing git push from pycharm
# Second line from github


class fileuploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text=
                                 "Please upload Excel only."
                                 " By default duplicate entries will be removed from excel file.")
    # task = serializers.CharField()