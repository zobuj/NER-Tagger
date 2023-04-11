from django.urls import path
from . import views

urlpatterns = [
    path('ner/process_paragraphs/', views.process_paragraphs, name='process_paragraphs'),
]