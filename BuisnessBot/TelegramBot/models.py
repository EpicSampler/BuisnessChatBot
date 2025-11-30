import os
import django
from django.conf import settings
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(project_root)
sys.path.append(project_root)

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BuisnessBot.settings')

if not settings.configured:
    django.setup()

from django.db import models

class Answers(models.Model):
    question = models.CharField('Вoпрос')
    answer = models.CharField('Ответ')


class Users(models.Model):
    name = models.CharField('ФИО')
    city = models.CharField('Город')
    place = models.CharField('Должность')
    organization = models.CharField('Название организации')
    special_code = models.SlugField('Код сотрудника')


class Organisations(models.Model):
    name = models.CharField('Название')
    city = models.CharField('Город')
    director = models.CharField('Директор', null=True)
    users = models.ManyToManyField(Users, 'Работники')