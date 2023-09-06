from django.urls import path
from . import views
urlpatterns = [
    path('', views.upload_pdf, name='home'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('process_question/', views.process_question, name='process_question'),
]
