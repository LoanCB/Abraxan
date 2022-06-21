from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from nifleur.models import ContractRequest, Speaker, Discipline


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


def contract_requests_list(request):
    contract_requests = ContractRequest.objects.all()
    return render(request, 'nifleur/contract_requests.html', {'contract_requests': contract_requests})


def speakers_list(request):
    speakers = Speaker.objects.all()
    return render(request, 'nifleur/speakers.html', {'speakers': speakers})


def speaker_details(request, speaker_id):
    speaker = get_object_or_404(Speaker, id=speaker_id)
    return render(request, 'nifleur/speaker_details.html', {'speaker': speaker})


def discipline_list(request):
    disciplines = Discipline.objects.all()
    return render(request, 'nifleur/disciplines.html', {'disciplines': disciplines})
