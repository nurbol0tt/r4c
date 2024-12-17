from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from customers.models import Customer
from orders.forms import OrderForm
from orders.models import Order
from robots.models import Robot


def create_order(request):
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if not form.is_valid():
            raise ValidationError("Данные формы не валидны. Пожалуйста, проверьте введенные данные.")
        customer_email = form.cleaned_data['customer_email']
        robot_serial = form.cleaned_data['robot_serial']
        customer, _ = Customer.objects.get_or_create(email=customer_email)

        robot = Robot.objects.filter(serial=robot_serial).first()
        if robot:
            return HttpResponse("Ваш заказ был принят!")

        Order.objects.create(customer=customer, robot_serial=robot_serial)
        return redirect('order_success')

    return render(request, 'create_order.html', {'form': form})


def order_success(request):
    return HttpResponse("Ваш заказ успешно создан! Мы уведомим вас, как только робот станет доступен.")