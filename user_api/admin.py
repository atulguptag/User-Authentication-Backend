from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.CinemaHall)
admin.site.register(models.Movie)
admin.site.register(models.Ticket)
admin.site.register(models.Show)
admin.site.register(models.Cinema)