from django.shortcuts import render, redirect
from .models import Testimonial, Appointment
from .forms import AddTestimonial, AddAppointment
from django.contrib import messages
import telebot


# Create your views here.


bot = telebot.TeleBot('6495492116:AAGgnn3NGhYdGA9_NizSHw8NdbADcDbhS5A')


def home(request):
    return render(
        request,
        'home.html',
        {'page_name': 'Стоматология на Первомайской'},
    )


def contacts(request):
    return render(request, 'contacts.html', {'page_name': 'Контакты'})


def appointment(request):
    if request.method == 'POST':
        appointment_form = AddAppointment(request.POST)

        if appointment_form.is_valid():
            new_appointment = Appointment()

            new_appointment.name = appointment_form.cleaned_data['name']
            new_appointment.email = appointment_form.cleaned_data['email']
            new_appointment.phone = appointment_form.cleaned_data['phone']
            new_appointment.service = appointment_form.cleaned_data['service']
            new_appointment.message = appointment_form.cleaned_data['message']

            new_appointment.save()

            bot.send_message(
                '894248983',
                f'\
{new_appointment.name}\n\
{new_appointment.email}\n\
{new_appointment.phone}\n\
{new_appointment.service}\n\
{new_appointment.message}\
',
            )

            return redirect('successful_appointment')
    else:
        appointment_form = AddAppointment()

    return render(
        request,
        'appointment.html',
        {
            'page_name': 'Записаться на прием',
            'appointment_form': appointment_form,
        },
    )


def successful_appointment(request):
    return render(
        request,
        'successful_appointment.html',
        {'page_name': 'Записаться на прием'},
    )


def services(request):
    return render(request, 'services.html', {'page_name': 'Услуги'})


def testimonials(request):
    all_testimonials = Testimonial.objects.all()

    if request.method == 'POST':
        testimonial_form = AddTestimonial(request.POST)

        if testimonial_form.is_valid():
            new_testimonial = Testimonial()

            new_testimonial.name = testimonial_form.cleaned_data['name']
            new_testimonial.service = testimonial_form.cleaned_data['service']
            new_testimonial.testimonial = \
                testimonial_form.cleaned_data['testimonial']

            new_testimonial.save()

            return redirect('testimonials')
    else:
        testimonial_form = AddTestimonial()

    return render(
        request,
        'testimonials.html',
        {
            'all_testimonials': all_testimonials,
            'page_name': 'Отзывы',
            'testimonial_form': testimonial_form,
        },
    )


def examples(request):
    return render(
        request,
        'examples.html',
        {'page_name': 'Примеры работ'},
    )


def about(request):
    return render(request, 'about.html', {'page_name': 'О клинике'})
