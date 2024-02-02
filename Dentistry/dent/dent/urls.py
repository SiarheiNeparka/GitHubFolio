"""
URL configuration for dent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import main.views as main_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", main_views.home, name='home'),
    path("contacts/", main_views.contacts, name='contacts'),
    path("appointment/", main_views.appointment, name='appointment'),
    path(
        "successful_appointment/",
        main_views.successful_appointment,
        name='successful_appointment',
    ),
    path("services/", main_views.services, name='services'),
    path("testimonials/", main_views.testimonials, name='testimonials'),
    path("examples/", main_views.examples, name='examples'),
    path("about/", main_views.about, name='about'),
]
