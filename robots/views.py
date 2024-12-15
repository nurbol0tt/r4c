import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import RobotForm
from .models import Robot

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
