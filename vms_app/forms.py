from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput, TimeInput


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ["is_working", "created_by", "created_on", "updated_by", "updated_on"]
        widgets = {
            'fc_date': DateInput(attrs={'type': 'date'}),
            'insurance': DateInput(attrs={'type': 'date'}),
            'puc': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = "__all__"


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = "__all__"


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ("zone", "ward", "route", "supervisor", "time_estimation", "km_estimation")


class EmployeeRegistrationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'password1', 'password2', 'is_superuser', 'is_zonal_manager', 'is_mechanic', 'contact', 'address', 'remark']

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': '3'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'image', 'contact', 'address', 'remark']

    def __init__(self, *args, **kwargs):
        super(EmployeeEditForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': '3'})
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift_name', 'vehicle',  'out_km', 'routes', 'driver', 'start_image']


class ShiftStartForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['shift_name', 'vehicle', 'routes', 'out_km', 'start_image', 'driver']


class RotateTripForm(forms.ModelForm):
    class Meta:
        model = TripHistory
        fields = ['wet_waste', 'recyclable_waste', 'dry_waste', 'inerts', 'household_hazard', 'green_garbages', 'other_waste', 'destination', 'trip_remark']


class ShiftEndForm(forms.Form):
    wet_waste = forms.IntegerField(initial=0) 
    recyclable_waste = forms.IntegerField(initial=0) 
    dry_waste = forms.IntegerField(initial=0) 
    inerts = forms.IntegerField(initial=0) 
    household_hazard = forms.IntegerField(initial=0) 
    green_garbages = forms.IntegerField(initial=0) 
    other_waste = forms.IntegerField(initial=0) 
    destination = forms.ChoiceField()
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    # trip_load = forms.IntegerField() 
    trip_remark = forms.CharField(max_length=250, required=False)
    shift_remark = forms.CharField(max_length=250, required=False)
    in_km = forms.FloatField()
    end_image = forms.ImageField(required=False)

    # class Meta:
    #     widgets = {
    #         'end_time': DateTimeInput()
    #     }
    

class CustomDateFilterForm(forms.Form):
    start = forms.DateField()
    end = forms.DateField()


class TransferRegisterForm(forms.ModelForm):
    class Meta:
        model = TransferRegister
        fields = ['vehicle', 'request_date', 'from_zone', 'to_zone', 'requested_by', 'reason']
        widgets = {
            'request_date': DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TransferRegisterForm, self).__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs.update({'rows': '3'})


class TransferRegisterStatusForm(forms.ModelForm):
    class Meta:
        model = TransferRegister
        fields = ['vehicle', 'request_date', 'from_zone', 'to_zone', 'requested_by', 'reason', 'reacted_date', 'reacted_by', 'status', 'remark', 'log_no']
        widgets = {
            'reacted_by': forms.HiddenInput(),
            'request_date': DateInput(attrs={'type': 'date'}),
            'reacted_date': DateInput(attrs={'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        super(TransferRegisterStatusForm, self).__init__(*args, **kwargs)
        self.fields['reason'].widget.attrs.update({'rows': '3'})


class AccidentLogForm(forms.ModelForm):
    class Meta:
        model = AccidentLog
        fields = '__all__'
        widgets = {
            'accident_time': DateTimeInput()
        }


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = '__all__'


class TripHistoryForm(forms.ModelForm):
    class Meta:
        model = TripHistory
        fields = ('trip_remark',)


class FuelMasterForm(forms.ModelForm):
    
    class Meta:
        model = FuelMaster
        fields = ("vehicle", "fuel_type", "fuel_km", "fuel_date", "fuel_quantity", "fuel_cost",)
        widgets = {
            'fuel_date': DateInput(attrs={'type': 'date'}),
        }


class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ('vehicle', 'workshop', 'work', 'zonal_manager_remark')
    
    def __init__(self, *args, **kwargs):
        super(JobCardForm, self).__init__(*args, **kwargs)
        self.fields['zonal_manager_remark'].widget.attrs.update({'rows': '3'})


class SpareRequestForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ('spares',)


class SpareApproveForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ('spares', 'spare_code', 'cost', 'approval_remark')


class StartJobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ('mechanics',)

    # def __init__(self, *args, **kwargs):
    #     super(EndJobCardForm, self).__init__(*args, **kwargs)
    #     self.fields['remark'].widget.attrs.update({'rows': '3'})


class EndJobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = ('remark',)

    def __init__(self, *args, **kwargs):
        super(EndJobCardForm, self).__init__(*args, **kwargs)
        self.fields['remark'].widget.attrs.update({'rows': '3'})


class MaintenanceSchedulesForm(forms.ModelForm):
    class Meta:
        model = MaintenanceSchedules
        fields = "__all__"
        widgets = {
            'scheduled_date': DateInput(attrs={'type': 'date'}),
        }


class DestinationLocationForm(forms.ModelForm):
    class Meta:
        model = DestinationLocation
        fields = "__all__"
