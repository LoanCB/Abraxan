from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from nifleur.forms import CustomUserCreationForm


@login_required
def home(request):
    return render(request, 'nifleur/home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.error(request, 'Utilisateur ou mot de passe incorrect')
            return redirect(login_user)

    return render(request, 'nifleur/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, "Vous avez bien été déconnecté")
    return redirect(login_user)


@login_required
def admin_management(request):
    form = CustomUserCreationForm()
    if form.is_valid():
        form.save()
        messages.success(request, "L'utilisateur a bien été créé")
    return render(request, 'nifleur/admin_management.html', {'form': form})
