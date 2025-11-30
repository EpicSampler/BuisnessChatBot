from django.db import models

class Answers(models.Model):
    question = models.CharField('Вoпрос')
    answer = models.CharField('Ответ')