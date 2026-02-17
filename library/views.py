from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, RegistrationForm, UserSettingsForm
from .models import Borrow


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
