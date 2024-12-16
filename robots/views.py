import json
import datetime

from django.db.models.aggregates import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Robot

from .forms import RobotForm

@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = RobotForm(data)
            if form.is_valid():
                form.save()
                return JsonResponse(form.cleaned_data, status=201)
            else:
                return JsonResponse(form.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        form = RobotForm()
    return render(request, 'robots.html', {'form': form})

def download_robot_summary(request):
    today = datetime.date.today()
    last_week_start = today - datetime.timedelta(days=7)

    # Группировка данных и подсчёт записей
    data = Robot.objects.all().values(
        'model', 'version'
    ).annotate(total=Count('id')).order_by('model', 'version')

    wb = Workbook()
    sheet_mapping = {}

    for entry in data:
        model = entry['model']
        version = entry['version']
        total = entry['total']

        if model not in sheet_mapping:
            sheet = wb.create_sheet(title=model)
            sheet_mapping[model] = sheet

            sheet.append(['Модель', 'Версия', 'Количество за неделю'])

        sheet_mapping[model].append([model, version, total])

    if not sheet_mapping:
        default_sheet = wb.active
        default_sheet.title = "Summary"
        default_sheet.append(["Нет данных за последние 7 дней"])

    if "Sheet" in wb.sheetnames and len(wb.sheetnames) > 1:
        wb.remove(wb["Sheet"])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="robot_summary_{today}.xlsx"'
    wb.save(response)

    return response


def download_summary_page(request):
    return render(request, 'upload.html')
