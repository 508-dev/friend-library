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

    # Borrow management
    path("requests/", views.borrow_requests_view, name="borrow_requests"),
    path("lendings/", views.current_lendings_view, name="current_lendings"),
    path("borrow/<int:borrow_id>/approve/", views.borrow_approve_view, name="borrow_approve"),
    path("borrow/<int:borrow_id>/deny/", views.borrow_deny_view, name="borrow_deny"),
    path("borrow/<int:borrow_id>/mark-lent/", views.borrow_mark_lent_view, name="borrow_mark_lent"),
    path("borrow/<int:borrow_id>/mark-returned/", views.borrow_mark_returned_view, name="borrow_mark_returned"),

    # Public lending pages (no login required)
    path("lend/<str:lending_hash>/", views.public_lending_page, name="public_lending"),
    path("lend/<str:lending_hash>/set-name/", views.public_set_borrower_name, name="public_set_name"),
    path("lend/<str:lending_hash>/<int:item_id>/", views.public_item_detail, name="public_item_detail"),
    path("lend/<str:lending_hash>/<int:item_id>/request/", views.public_request_borrow, name="public_request_borrow"),
]
