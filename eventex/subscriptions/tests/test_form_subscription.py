from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(
            expected, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits"""
        form = self._make_validated_form(cpf='ABC5678901')
        self.assertFormErrorCode(form, 'cpf', 'cpf_digits')

    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits"""
        form = self._make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'cpf_length')

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def _make_validated_form(self, cpf):
        data = dict(name="Henrique Bastos", cpf=cpf,
                    email="henrique@bastos.net", phone="21-99618-6180")
        form = SubscriptionForm(data)
        form.is_valid()
        return form
