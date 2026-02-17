from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Item, Borrow


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "is_approved",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    list_filter = ["is_approved", "is_staff", "is_superuser", "is_active"]
    search_fields = ["username"]
    ordering = ["-date_joined"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Lending Settings",
            {
                "fields": (
                    "is_approved",
                    "lending_hash",
                    "show_borrowed_items",
                    "show_borrower_name",
                    "show_lending_history",
                    "show_history_borrower_names",
                )
            },
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Approval",
            {"fields": ("is_approved",)},
        ),
    )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "is_available", "created_at"]
    list_filter = ["is_available", "owner"]
    search_fields = ["title", "short_description"]
    ordering = ["-created_at"]


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ["item", "borrower_name", "status", "requested_at"]
    list_filter = ["status"]
    search_fields = ["borrower_name", "item__title"]
    ordering = ["-requested_at"]
