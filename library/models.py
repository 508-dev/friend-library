import secrets
from django.db import models
from django.contrib.auth.models import AbstractUser


def generate_lending_hash():
    return secrets.token_urlsafe(16)


class User(AbstractUser):
    """Custom user model for lenders."""

    is_approved = models.BooleanField(
        default=False,
        help_text="Whether this user has been approved by an admin to use the system.",
    )
    lending_hash = models.CharField(
        max_length=32,
        unique=True,
        default=generate_lending_hash,
        help_text="Secret hash for the user's public lending page URL.",
    )

    # Visibility settings for the public lending page
    show_borrowed_items = models.BooleanField(
        default=True,
        help_text="Whether friends can see currently borrowed items on the lending page.",
    )
    show_borrower_name = models.BooleanField(
        default=False,
        help_text="Whether friends can see who is currently borrowing an item.",
    )
    show_lending_history = models.BooleanField(
        default=False,
        help_text="Whether friends can see lending history on item detail pages.",
    )
    show_history_borrower_names = models.BooleanField(
        default=False,
        help_text="Whether friends can see borrower names in lending history.",
    )

    def regenerate_lending_hash(self):
        self.lending_hash = generate_lending_hash()
        self.save(update_fields=["lending_hash"])

    def __str__(self):
        return self.username


class Item(models.Model):
    """An item available for lending."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500, blank=True)
    long_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="items/", blank=True)
    borrow_time_limit = models.CharField(
        max_length=100,
        blank=True,
        help_text="Freeform text describing how long items can be borrowed.",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this item is available for borrowing (can be toggled by owner).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_currently_borrowed(self):
        return self.borrows.filter(status=Borrow.Status.LENT_OUT).exists()

    @property
    def current_borrow(self):
        return self.borrows.filter(status=Borrow.Status.LENT_OUT).first()


class Borrow(models.Model):
    """A borrow request or active loan."""

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved (Pending Pickup)"
        DENIED = "denied", "Denied"
        LENT_OUT = "lent_out", "Lent Out"
        RETURNED = "returned", "Returned"

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="borrows")
    borrower_name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED,
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    lent_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-requested_at"]
        verbose_name_plural = "borrows"

    def __str__(self):
        return f"{self.borrower_name} - {self.item.title} ({self.get_status_display()})"
