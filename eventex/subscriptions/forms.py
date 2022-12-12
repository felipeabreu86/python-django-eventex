from django import forms
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'cpf_digits')
    if len(value) != 11:
        raise ValidationError('CPF deve ter 11 números', 'cpf_length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')
