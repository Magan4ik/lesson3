from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts import forms, models
from accounts.utils import send_activation_email

User = get_user_model()

def has_profile(user: User) -> bool:
    return not hasattr(user, 'profile')


@require_http_methods(["GET", "POST"])
def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('accounts:test')

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, email=email, password=password)

            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)

            if user:
                login(request, user)
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect('accounts:test')
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'accounts/login.html', {'form': form})
        else:
            messages.error(request, 'Invalid form data')
            return render(request, 'accounts/login.html', {'form': form})

    form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('accounts:login')


def test_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


@require_http_methods(["GET", "POST"])
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('accounts:test')
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            send_activation_email(user)
            url = reverse("accounts:activate_token", args=[user.username])
            return redirect(url)
        return render(request, 'accounts/signup.html', {'form': form})

    form = forms.RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def activate_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    if user.is_active:
        messages.info(request, "Account has already been verified")
        return redirect("accounts:test")
    splited_email = user.email.split("@")
    first_part = splited_email[0][:4]
    domen_part = splited_email[1]
    blured_email = f"{first_part}{'*'*(len(splited_email[0])-4)}@{domen_part}"
    if request.method == "POST":
        if request.POST.get("token", "") == user.register_token:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Account activated successfully")
            return redirect("accounts:create_profile")
        else:
            messages.error(request, f"The token does not match. A new token has been sent to you at {blured_email}")
            send_activation_email(user)

            return render(request, "accounts/token.html", {"blured_email": blured_email})

    return render(request, "accounts/token.html", {"blured_email": blured_email})

@login_required
@user_passes_test(has_profile, login_url="accounts:test")
@require_http_methods(["GET", "POST"])
def create_profile_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("accounts:test")
        return render(request, "accounts/create_profile.html", {"form": form})
    form = forms.ProfileForm()
    return render(request, "accounts/create_profile.html", {"form": form})


@login_required
def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    if not (profile := models.Profile.objects.filter(user=user)).exists():
        return redirect("accounts:create_profile")
    return render(request, "accounts/profile.html", {"profile": profile[0]})


@login_required
def follow_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    follow, created = models.Follow.objects.get_or_create(author=request.user, user=user)
    if not created:
        follow.delete()
    url = reverse("accounts:profile", args=[username])
    return redirect("accounts:profile", username=username)

@login_required
@require_http_methods(["GET", "POST"])
def edit_profile_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(models.Profile, user=user)
    if request.user == user or request.user.is_superuser:
        if request.method == 'POST':
            form = forms.ProfileForm(instance=profile, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "The profile has been successfully updated")
                return redirect("accounts:profile", username=username)
            else:
                return render(request, "accounts/edit_profile.html", {'form': form, "username": username})
    else:
        messages.warning(request, "You don't have permission to edit this profile.")
        return redirect("accounts:profile", username=username)

    form = forms.ProfileForm(instance=profile)
    return render(request, "accounts/edit_profile.html", {"form": form, "username": username})

@login_required
@require_http_methods(["GET", "POST"])
def change_password_view(request: HttpRequest, username: str) -> HttpResponse:
    if request.user.username != username:
        messages.warning(request, "You don't have permission to change this password.")
        return redirect("accounts:profile", username=username)
    if request.method == "POST":
        form = forms.PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been successfully changed")
            return redirect("accounts:profile", username=username)
        else:
            return render(request, "accounts/change_password.html", {'form': form})

    form = forms.PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})

@require_http_methods(["GET","POST"])
def verify_email_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        user = get_object_or_404(User, email=request.POST.get("email"))
        user.is_active = False
        user.save()
        send_activation_email(user)
        return redirect("accounts:activate_token")
    return render(request, "accounts/verify_email.html")
