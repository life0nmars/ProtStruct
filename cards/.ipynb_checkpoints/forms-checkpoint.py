"""
Формы для квизов и тестов
"""
from django import forms

class CardForm(forms.Form):
    """
    Форма для распознавания аминокислотных остатков
    """
    res1 = forms.CharField(label='Three-letter abbreviation', max_length=3)
    res2 = forms.CharField(label='One-letter abbreviation', max_length=1)

class SequenceForm(forms.Form):
    """
    Форма для проверки последовательности белка из ДНК
    """
    answer = forms.CharField(label='Your protein', max_length=16)

class NucleotideForm(forms.Form):
    """
    Форма для проверки правильности нуклеотида
    """
    answer1 = forms.CharField(label='Abbreviation of the nucleotide', max_length=1)
    answer2 = forms.CharField(label='Full name', max_length=30)
