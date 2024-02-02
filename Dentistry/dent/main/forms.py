from typing import Any
from django import forms
from .models import SERVICE_TYPES


class AddTestimonial(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Ваше имя"}
    ))
    service = forms.ChoiceField(
        choices=SERVICE_TYPES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    testimonial = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": "7",
            "placeholder": "Отзыв",
        }))

    def clean_name(self):
        return self.cleaned_data['name'].strip().capitalize()

    def clean_testimonial(self):
        return self.cleaned_data['testimonial'].strip()


class AddAppointment(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Ваше имя"}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Ваш email"}
    ))
    phone = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Ваш номер телефона"}
    ))
    service = forms.ChoiceField(
        choices=SERVICE_TYPES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": "5",
            "placeholder": "Дополнительная информация (не обязательно)",
        }))

    def clean_name(self):
        return self.cleaned_data['name'].strip().capitalize()

    def clean_message(self):
        return self.cleaned_data['message'].strip()
