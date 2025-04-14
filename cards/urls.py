# cards/urls.py
"""
Стандартный файл, в котором соотносятся url с видами
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="cards/base.html"), name="home"),
    path('amino_acid', views.CheckStructureView.as_view(), name='check_structure'),
    path('protein_sequence', views.CheckSequenceView.as_view(), name='check_sequence'),
    path('nucleobase', views.CheckNucleotideView.as_view(), name='check_nucleobase'),
    path('nucleobase_info', views.InfoPage.as_view(), name='info_nucleobase')
]
