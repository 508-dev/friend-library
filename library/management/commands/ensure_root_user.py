"""
Management command to ensure root user exists.
Creates the root superuser from environment variables if it doesn't exist.
"""

import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Ensures the root superuser exists (creates from env vars if missing)"

    def handle(self, *args, **options):
        username = os.environ.get("ROOT_USERNAME")
        password = os.environ.get("ROOT_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ROOT_USERNAME and ROOT_PASSWORD environment variables not set. "
                    "Skipping root user creation."
                )
            )
            return

        user = User.objects.filter(username=username).first()
        if user:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Root user '{username}' password updated.")
            )
            return

        User.objects.create_superuser(
            username=username,
            password=password,
            is_approved=True,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Root user '{username}' created successfully.")
        )
