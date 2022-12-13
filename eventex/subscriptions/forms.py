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
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.CharField(label='Telefone', required=False)

    def clean_name(self):
        """
        O formulário procura por qualquer função 'clean_' + CAMPO para 
        procurar por uma complementação do campo
        """
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)

    def clean(self):
        """
        Função Clean do Formulário que é chamada após a validação de todos os 
        campos. É útil para validações conjuntas dos campos.
        """
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone')
        return self.cleaned_data
