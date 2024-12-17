import json

from django.db.models.aggregates import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Robot
from django.utils import timezone
from datetime import timedelta

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
    week_ago = timezone.now() - timedelta(days=7)

    data = (
        Robot.objects.filter(created__gte=week_ago)
        .values('model', 'version')
        .annotate(total=Count('id'))
        .order_by('model')
    )

    wb = Workbook()
    sheet = wb.active
    sheet.title = "Сводка по моделям"

    sheet.append(['Модель', 'Версия', 'Количество за неделю'])

    for entry in data:
        model = entry['model']
        version = entry['version']
        total = entry['total']
        sheet.append([model, version, total])

    if not data:
        sheet.append(["Нет данных за последние 7 дней"])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="robot_summary.xlsx"'
    wb.save(response)

    return response


def download_summary_page(request):
    return render(request, 'upload.html')
