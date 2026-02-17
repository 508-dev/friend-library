from django.shortcuts import render


def home(request):
    """Landing page - shows marketing info or redirects to dashboard if logged in."""
    if request.user.is_authenticated:
        # Will redirect to dashboard in phase 2
        pass
    return render(request, "library/home.html")
