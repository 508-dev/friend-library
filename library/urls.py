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

    # Item management
    path("items/", views.item_list_view, name="item_list"),
    path("items/add/", views.item_add_view, name="item_add"),
    path("items/<int:item_id>/edit/", views.item_edit_view, name="item_edit"),
    path("items/<int:item_id>/delete/", views.item_delete_view, name="item_delete"),
    path("items/<int:item_id>/toggle-availability/", views.item_toggle_availability_view, name="item_toggle_availability"),

    # Public lending pages will be added in phase 4
]
