from django.db import models

# Create your models here.


SERVICE_TYPES = [
    ('Терапия', 'Терапия'),
    ('Хирургия/имплантация', 'Хирургическое лечение и имплантация'),
    ('Ортопедия', 'Ортопедическое лечение'),
]


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=19)
    service = models.CharField(max_length=20, choices=SERVICE_TYPES)
    message = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.service


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=20, choices=SERVICE_TYPES)
    testimonial = models.TextField()

    def __str__(self) -> str:
        return f'{self.name} ({self.service})'
