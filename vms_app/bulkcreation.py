from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from VMS.settings import BASE_DIR
from .serializers import fileuploadSerializer
import pandas as pd
import os
from .models import Employee, Vehicle, Vehicles_RTO_details
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime
import json


input_date_format1 = '%d-%m-%Y'  # 30-12-2023
input_date_format2 = '%d/%m/%Y'  # 30/12/2023
input_date_format3 = '%d-%m-%y'  # 30-12-23
input_date_format4 = '%Y-%m-%d'  # 2024-12-31


# one
# Everything is common
def storeFile(file):
    '''
    :param file: file (usually .xlsx)
    :action: check file size 10MB; store file in media
    :return: Absolute path of stored file
    '''
    print('Executing storeFile')
    store_path = os.path.join(BASE_DIR, 'media', 'uplaoded_files')
    max_file_size_bytes = 10 * 1024 * 1024  # 10 MB
    if file.size > max_file_size_bytes:
        raise ValidationError(f"File size exceeds the limit of {max_file_size_bytes} bytes.")

    if not os.path.exists(store_path):
        os.makedirs(store_path)
    fs = FileSystemStorage(location=store_path)
    current_time = timezone.now().strftime('%Y%m%d%H%M%S')
    file_name = f"{current_time}_{file.name}"
    filename = fs.save(file.name, file)
    sourcefilepath = os.path.join(store_path, filename)
    print('sourcefilepath', sourcefilepath, sep='\n')
    return sourcefilepath


# three
# Everything is common
def reader(sourcefilepath):
    print('executing reader')
    try:
        df_original = pd.read_excel(sourcefilepath)
        return df_original
    except:
        return False


# two
# Everything is common
def timer(sourcefilepath):
    print('executing timer')
    import time
    start_time = time.time()
    while not os.path.exists(sourcefilepath) and (time.time() - start_time) < 300:
        time.sleep(2)
        # print('timer is checking')
    if not os.path.exists(sourcefilepath):
        return None
    else:
        return reader(sourcefilepath)


# five
def columCroper(df, set_of_heads):
    print('executing columCroper')
    file_needed_headers = list(set_of_heads)
    df = df[file_needed_headers]
    return df


# four
def header_aligner(df, set_of_heads):
    print('header_aligner')
    # checking heads
    df_header = set(df.keys())
    if set_of_heads.issubset(df_header):
        return columCroper(df, set_of_heads)
    else:
        return False


# six
def createEmployee(df):
    print('createEmployee')
    '''Create obj if not exist. if existed, it will update the object'''
    failure_indices = {}
    for index, row in df.iterrows():
        name = row['name']
        employee_id = row['employee_id']
        is_staff = row['is_staff']
        email = None if pd.isna(row['email']) else row['email']  # Handling blank cells returning nan
        contact = None if pd.isna(row['contact']) else row['contact']  # Handling blank cells returning nan

        try:
            obj, created = Employee.objects.get_or_create(employee_id=employee_id, defaults={
                'name': name,
                'is_staff': is_staff,
                'email': email,
                'contact': contact

            })
            if not created:
                obj.name = name
                obj.is_staff = is_staff
                obj.email = email
                obj.contact = contact
                employee = obj.save()
                employee.set_password('Welcome@123')
                employee.save()

        except Exception as e:
            failure_indices[index + 2] = e
            print(f"Error creating object from row {index + 2}: {e}")
    return failure_indices


# six
def createVehicle(df):
    failure_indices = {}
    for index, row in df.iterrows():
        # vehicle
        vehicle_number = row['vehicle_number']
        is_spare = row['is_spare']
        load_estimation = None if pd.isna(row['load_estimation']) else row['load_estimation']
        supervisor_employee_id = None if pd.isna(row['supervisor']) else row['supervisor']
        supervisor = Employee.objects.filter(employee_id=supervisor_employee_id).first()

        try:
            vehicle_obj, created_vehicle = Vehicle.objects.get_or_create(vehicle_number=vehicle_number, defaults={
                'is_spare': is_spare,
                'load_estimation': load_estimation,
                'supervisor': supervisor
            })
            if not created_vehicle:
                vehicle_obj.is_spare = is_spare
                vehicle_obj.load_estimation = load_estimation
                vehicle_obj.supervisor = supervisor
                vehicle_obj.save()

        except Exception as e:
            failure_indices[index + 2] = e
            print(f"Error creating object from row {index + 2}: {e}")
    return failure_indices


# six
def createVehicleDetails(df):
    failure_indices = {}
    for index, row in df.iterrows():
        vehicle_number = row['vehicle_number']
        vehicle_obj = Vehicle.objects.get(vehicle_number=vehicle_number)
        chassis_number = None if pd.isna(row['chassis_number']) else row['chassis_number']
        vehicle_model = None if pd.isna(row['vehicle_model']) else row['vehicle_model']
        vehicle_type = None if pd.isna(row['vehicle_type']) else row['vehicle_type']
        engine_number = None if pd.isna(row['engine_number']) else row['engine_number']
        fc_date = None if pd.isna(row['fc_date']) else row['fc_date']
        insurance = None if pd.isna(row['insurance']) else row['insurance']
        puc = None if pd.isna(row['puc']) else row['puc']
        try:
            vehicle_details, created = Vehicles_RTO_details.objects.get_or_create(vehicle=vehicle_obj, defaults={
                'chassis_number': chassis_number,
                'vehicle_model': vehicle_model,
                'vehicle_type': vehicle_type,
                'engine_number': engine_number,
                'fc_date': fc_date,
                'insurance': insurance,
                'puc': puc
            })
            if not created:
                vehicle_details.chassis_number = chassis_number
                vehicle_details.vehicle_model = vehicle_model
                vehicle_details.vehicle_type = vehicle_type
                vehicle_details.engine_number = engine_number
                vehicle_details.fc_date = fc_date
                vehicle_details.insurance = insurance
                vehicle_details.puc = puc
                vehicle_details.save()

        except Exception as e:
            failure_indices[index + 2] = e
            print(f"Error creating object from row {index + 2}: {e}")
    return failure_indices


# alone
def format_date(df, columns_to_date_type, input_date_format=input_date_format1):
    # columns_to_date_type = ['mystringtodate']
    def process_date(x):
        try:
            # convert string to date object
            return datetime.strptime(str(x), input_date_format).date()
        except (ValueError, TypeError):
            try:
                # convert datetime object to date object
                return x.date()
            except:
                # else 'Not a date or date format mismatch'
                return None

    for column in columns_to_date_type:
        df[column] = df[column].apply(process_date)

    return df


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def bulkcreateEmployee(request):
    print('Executing upload function')
    serializers = fileuploadSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    file = serializers.validated_data['file']

    stored_file = storeFile(file)  # trying to save the upload excel
    df_original = timer(stored_file)  # Waiting for 5min to finish upload and then read file
    # df_original will be a dataframe if everything is okay or else it will be None or False
    if isinstance(df_original, pd.DataFrame) and len(df_original) > 0:  # Alert "if df_original:" will not work here
        df = df_original.drop_duplicates()
    else:
        os.remove(stored_file)
        return Response({'Error': 'Something wrong with file'})
    set_of_heads = {'name', 'employee_id', 'is_staff', 'contact', 'email'}

    df = header_aligner(df, set_of_heads)  # Now df can be either dataframe or False
    if isinstance(df, pd.DataFrame):
        # df = format_date(df, input_date_format1)
        failure_indices = createEmployee(df)
        failure_indices_json = json.dumps(failure_indices, indent=4, sort_keys=True, default=str)
        print(failure_indices)
        # return HttpResponse(failure_indices.items())
        os.remove(stored_file)
        return Response(failure_indices_json)

    else:
        os.remove(stored_file)
        return Response({'Error': 'Please check head of uploaded Excel file'})

@api_view(['POST'])
def set_userpassword(request):
    '''
    {'userlist': [empid, empid, ...]}
    '''
    print('executing set user password')
    data = request.data
    users = data.get('userlist')
    print(users)
    for empid in users:
        print(empid)
        try:
            user = Employee.objects.get(employee_id=empid)
            print(user)
            user.set_password('Welcome@123')
            user.save()
        except:
            print(f'Failure empid-->{empid}')
    return Response({})


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def bulkcreateVehicle(request):
    print('Executing upload function')
    serializers = fileuploadSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    file = serializers.validated_data['file']
    stored_file = storeFile(file)  # trying to save the upload excel
    df_original = timer(stored_file)
    if isinstance(df_original, pd.DataFrame) and len(df_original) > 0:  # Alert "if df_original:" will not work here
        df = df_original.drop_duplicates()
    else:
        os.remove(stored_file)
        return Response({'Error': 'Something wrong with file'})
    # set_of_heads = {'vehicle_number', 'is_spare', 'load_estimation', 'supervisor', 'chassis_number',
    #                 'vehicle_model', 'vehicle_type', 'engine_number', 'fc_date', 'insurance', 'puc'}
    set_of_heads = {'vehicle_number', 'is_spare', 'load_estimation', 'supervisor'}

    df = header_aligner(df, set_of_heads)  # Now df can be either dataframe or False
    if isinstance(df, pd.DataFrame):
        failure_indices = createVehicle(df)
        failure_indices_json = json.dumps(failure_indices, indent=4, sort_keys=True, default=str)
        print(failure_indices)
        # return HttpResponse(failure_indices.items())
        os.remove(stored_file)
        return Response(failure_indices_json)

    else:
        os.remove(stored_file)
        return Response({'Error': 'Please check head of uploaded Excel file'})


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def bulkcreateVehicleDetails(request):
    '''
    :param request: excel
    :return: create/update objects
    Warning: All dates should be 2024-12-31 format. Either it should be date format or it should "2024-12-31" kind str
    '''
    print('Executing upload function')
    serializers = fileuploadSerializer(data=request.data)
    serializers.is_valid(raise_exception=True)
    file = serializers.validated_data['file']

    stored_file = storeFile(file)  # trying to save the upload excel
    df_original = timer(stored_file)

    # Waiting for 5min to finish upload and then read file
    # df_original will be a dataframe if everything is okay or else it will be None or False
    print(df_original)
    if isinstance(df_original, pd.DataFrame) and len(df_original) > 0:  # Alert "if df_original:" will not work here
        df = df_original.drop_duplicates()
    else:
        # os.remove(stored_file)
        return Response({'Error': 'Something wrong with file'})
    set_of_heads = {'vehicle_number',  'chassis_number', 'vehicle_model', 'vehicle_type', 'engine_number', 'fc_date', 'insurance', 'puc'}

    df = header_aligner(df, set_of_heads)  # Now df can be either dataframe or False
    if isinstance(df, pd.DataFrame):
        columns_to_date_type = ['fc_date', 'insurance', 'puc']
        df = format_date(df, columns_to_date_type, input_date_format4)
        failure_indices = createVehicleDetails(df)
        failure_indices_json = json.dumps(failure_indices, indent=4, sort_keys=True, default=str)
        print(failure_indices)
        # return HttpResponse(failure_indices.items())
        os.remove(stored_file)
        return Response(failure_indices_json)

    else:
        os.remove(stored_file)
        return Response({'Error': 'Please check head of uploaded Excel file'})




