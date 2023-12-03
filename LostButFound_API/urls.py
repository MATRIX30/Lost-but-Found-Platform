from . import views
from django.urls import path

urlpatterns = [
    path("",views.index),
    path("search/",views.search,name="search"),
    path("sms/",views.sms, name="sms"),
    path("save/",views.save, name="save")
]
