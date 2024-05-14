```

def productivity_excel_report(filename, productivity):
    wb = Workbook()
    ws = wb.active
    ws.title = filename

    headers = ["Vehicle No.", "Start", "End", "Driver", "Estimation", "Production"]
    ws.append(headers)

    for i in productivity:
        ws.append(
            [i.vehicle.vehicle_number, i.start.strftime('%d/%m/%Y'), i.end.strftime('%d/%m/%Y'), i.driver, i.estimation,
             i.day_production])

    return wb


@login_required(login_url='login')
@active_required
def productivity_week_report(request):
    today = timezone.now()
    start_date = today - timezone.timedelta(days=today.weekday())
    end_date = start_date + timezone.timedelta(days=7)
    filename = today.strftime("Week-%W %B %Y")
    productivity = Productivity.objects.filter(
        start__date__gte=start_date,
        start__date__lte=end_date
    )

    if request.method == "POST":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "head": filename,
        "menu": "menu-productivity",
        "productivity_list": productivity
    }
    return render(request, 'vms_app/productivity_report.html', context)


@login_required(login_url='login')
@active_required
def productivity_month_report(request):
    today = timezone.now()
    current_year = today.year
    current_month = today.month
    productivity = Productivity.objects.filter(
        start__year=current_year,
        start__month=current_month
    )
    filename = today.strftime("%B %Y")

    if request.method == "POST":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "head": filename,
        "menu": "menu-productivity",
        "productivity_list": productivity
    }
    return render(request, 'vms_app/productivity_report.html', context)


@login_required(login_url='login')
@active_required
def productivity_custom_report(request):
    today = timezone.now()
    data = {
        "start": today,
        "end": today,
    }
    download = False

    if request.method == "POST":
        download = bool(request.POST.get('download', False))
        form = ProductivityReportForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

    productivity = Productivity.objects.filter(
        start__date__gte=data['start'],
        start__date__lte=data['end']
    )

    if download:
        filename = f"{data['start'].strftime('%d.%m.%Y')} - {data['end'].strftime('%d.%m.%Y')}"
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

        excel_report = productivity_excel_report(filename, productivity)
        excel_report.save(response)
        return response

    context = {
        "data": data,
        "head": "Custom Report",
        "menu": "menu-productivity",
        "productivity_list": productivity,
        "custom": True
    }
    return render(request, 'vms_app/productivity_report.html', context)

```