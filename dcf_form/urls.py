from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("valuation/",views.form,name="valuate"),
    path('evaluate/', views.valuate,name="evaluate"),
    path('getotp/', views.get_otp,name="getotp"),
    path('saveinfo/', views.save,name="saveinfo")
]
