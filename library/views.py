from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .forms import LoginForm, RegistrationForm, UserSettingsForm, ItemForm
from .models import Item, Borrow


def home(request):
    """Landing page - shows marketing info or redirects to dashboard if logged in."""
    if request.user.is_authenticated:
        return redirect("library:dashboard")
    return render(request, "library/home.html")


def login_view(request):
    """Login page for lenders."""
    if request.user.is_authenticated:
        return redirect("library:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            login(request, form.user)
            next_url = request.GET.get("next", "library:dashboard")
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, "library/login.html", {"form": form})


def logout_view(request):
    """Logout and redirect to home."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("library:home")


def register_view(request):
    """Registration request page."""
    if request.user.is_authenticated:
        return redirect("library:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Registration submitted! Please wait for an admin to approve your account.",
            )
            return redirect("library:registration_pending")
    else:
        form = RegistrationForm()

    return render(request, "library/register.html", {"form": form})


def registration_pending_view(request):
    """Shown after registration to confirm the request was received."""
    return render(request, "library/registration_pending.html")


@login_required
def dashboard_view(request):
    """Main dashboard for logged-in lenders."""
    user = request.user

    # Get recent borrow requests (requested status, limit 5)
    recent_requests = Borrow.objects.filter(
        item__owner=user,
        status=Borrow.Status.REQUESTED,
    ).select_related("item")[:5]

    # Get pending pickups (approved but not yet lent)
    pending_pickups = Borrow.objects.filter(
        item__owner=user,
        status=Borrow.Status.APPROVED,
    ).select_related("item")[:5]

    # Get current lendings (lent out)
    current_lendings = Borrow.objects.filter(
        item__owner=user,
        status=Borrow.Status.LENT_OUT,
    ).select_related("item")[:5]

    # Item counts
    total_items = user.items.count()
    available_items = user.items.filter(is_available=True).count()
    borrowed_items = user.items.filter(
        borrows__status=Borrow.Status.LENT_OUT
    ).distinct().count()

    context = {
        "recent_requests": recent_requests,
        "pending_pickups": pending_pickups,
        "current_lendings": current_lendings,
        "total_items": total_items,
        "available_items": available_items,
        "borrowed_items": borrowed_items,
        "lending_url": request.build_absolute_uri(f"/lend/{user.lending_hash}/"),
    }
    return render(request, "library/dashboard.html", context)


@login_required
def settings_view(request):
    """User settings page."""
    user = request.user

    if request.method == "POST":
        if "regenerate_hash" in request.POST:
            user.regenerate_lending_hash()
            messages.success(request, "Your lending link has been regenerated.")
            return redirect("library:settings")

        form = UserSettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings saved.")
            return redirect("library:settings")
    else:
        form = UserSettingsForm(instance=user)

    context = {
        "form": form,
        "lending_url": request.build_absolute_uri(f"/lend/{user.lending_hash}/"),
    }
    return render(request, "library/settings.html", context)


@login_required
def item_list_view(request):
    """View all items owned by the current user."""
    items = request.user.items.all()
    return render(request, "library/item_list.html", {"items": items})


@login_required
def item_add_view(request):
    """Add a new item."""
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, f'"{item.title}" has been added to your library.')
            return redirect("library:item_list")
    else:
        form = ItemForm()

    return render(request, "library/item_form.html", {
        "form": form,
        "is_edit": False,
    })


@login_required
def item_edit_view(request, item_id):
    """Edit an existing item."""
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{item.title}" has been updated.')
            return redirect("library:item_list")
    else:
        form = ItemForm(instance=item)

    return render(request, "library/item_form.html", {
        "form": form,
        "item": item,
        "is_edit": True,
    })


@login_required
def item_delete_view(request, item_id):
    """Delete an item with confirmation."""
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == "POST":
        title = item.title
        item.delete()
        messages.success(request, f'"{title}" has been removed from your library.')
        return redirect("library:item_list")

    return render(request, "library/item_delete.html", {"item": item})


@login_required
def item_toggle_availability_view(request, item_id):
    """Toggle item availability (HTMX endpoint)."""
    item = get_object_or_404(Item, id=item_id, owner=request.user)

    if request.method == "POST":
        item.is_available = not item.is_available
        item.save(update_fields=["is_available"])

        # Return updated button HTML for HTMX swap
        return render(request, "library/partials/item_availability_button.html", {
            "item": item,
        })
