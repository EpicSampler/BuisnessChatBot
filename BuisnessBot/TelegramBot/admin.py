from django.contrib import admin
from .models import Answers, Users, Organisations

# Register your models here.
admin.site.register(Answers)
admin.site.register(Users)
admin.site.register(Organisations)