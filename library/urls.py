from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    # Public pages
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("register/pending/", views.registration_pending_view, name="registration_pending"),

    # Dashboard (logged-in users)
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("settings/", views.settings_view, name="settings"),

    # Public lending pages will be added in phase 4
]
