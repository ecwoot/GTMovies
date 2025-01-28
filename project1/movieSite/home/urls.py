from django.urls import path
from . import views

#(idk real documentation guideline I'm sorry)

#contains the url path for the HOME app and calls in the index function
#in home/views.py
urlpatterns = [
    path('', views.index, name='home.index')
]