from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot


def send_robot_availability_email(customer_email, robot_model, robot_version):
    subject = "Робот доступен"
    message = (
        f"Добрый день!\n"
        f"Недавно вы интересовались нашим роботом модели {robot_model}, версии {robot_version}.\n"
        f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
    )
    send_mail(
        subject,
        message,
        'noreply@robotcompany.com',
        [customer_email],
        fail_silently=False,
    )


@receiver(post_save, sender=Robot)
def notify_customers_about_robot_availability(sender, instance, created, **kwargs):
    if created:
        orders = Order.objects.filter(robot_serial=instance.serial)
        for order in orders:
            print("CODES WORKING")
            customer_email = order.customer.email
            send_robot_availability_email(
                customer_email,
                robot_model=instance.model,
                robot_version=instance.version,
            )

