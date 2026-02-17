from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),
    # Auth will be added in phase 2
    # Lender dashboard will be added in phase 2
    # Public lending pages will be added in phase 4
]
