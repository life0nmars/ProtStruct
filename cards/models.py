# pylint: disable=too-few-public-methods.
#disable=no-member
"""
Архитектура БД
"""
from django.db import models

class Structure(models.Model):
    """
    Модель структуры: получаем PDB и картинку
    В будущем планирую задавать еще тип укладки структуры
    и использовать в других квизах и странице информации
    """
    objects = models.Manager()
    pdb = models.CharField(max_length=5)
    image = models.ImageField(upload_to='images/', blank = True, null = True)
    def __str__(self):
        return f"{self.pdb}"

class Card(models.Model):
    """
    Модель Карточка:
    здесь содержится информация об аминокислотном остатке,
    который выделен в какой-то из структур прошлой модели.
    Модель связана с предыдущей.
    res1 - полное название
    res2 - однобуквенный код а/к
    """
    objects = models.Manager()
    protein = models.ForeignKey(Structure, on_delete=models.CASCADE)
    structure_name = models.CharField(max_length=100)
    res1 = models.CharField(max_length=100)
    res2 = models.CharField(max_length=100)

class Sequence(models.Model):
    """
    Модель Последовательность:
    здесь содержится информация о последовательностях
    матрицы ДНК (question)
    и белка (answer)
    """
    objects = models.Manager()
    question = models.CharField(max_length=54)
    answer = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.question}"

class Nucleotide(models.Model):
    """
    Модель Нуклеотид:
    здесь содержится информация о нуклеотидах:
    Их изображение (question);
    однобуквенная аббривеатура (answer1);
    двухбуквенная аббривеатура (answer2)
    """
    objects = models.Manager()
    question = models.ImageField(upload_to='images/', blank = True, null = True)
    answer1 = models.CharField(max_length=1)
    answer2 = models.CharField(max_length=30)
