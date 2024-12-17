from django import forms

class OrderForm(forms.Form):
    customer_email = forms.EmailField(label="Ваш Email", max_length=255)
    robot_serial = forms.CharField(label="Серийный номер робота", max_length=5)
