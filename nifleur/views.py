from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from nifleur.forms import DisciplineForm, SpeakerForm, ContractRequestForm
from nifleur.models import ContractRequest, Speaker, Discipline, StructureCampus
from nifleur.utils import export_csv, short_datetime


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


def contract_request_detail(request, contract_id):
    contract = get_object_or_404(ContractRequest, id=contract_id)
    return render(request, 'nifleur/contract_request_details.html', {'contract': contract})


def create_contract_request(request):
    form = ContractRequestForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "La demande de contrat a bien été créée")
        return redirect(contract_request_detail)
    return render(request, 'nifleur/contract_request_form.html', {'form': form})


def export_contract_requests(request):
    contract_requests = ContractRequest.objects.all()
    data = []
    for contract in contract_requests:
        ttc = 'TTC' if contract.ttc else 'SST'
        alternating = 'Alternante' if contract.alternating else 'Initiale'
        data.append([
            short_datetime(contract.created_at), contract.structure_campus, contract.speaker, contract.comment,
            contract.status.label, contract.performance, contract.applied_rate, contract.rate_type, ttc,
            contract.hourly_volume, short_datetime(contract.started_at), short_datetime(contract.ended_at),
            contract.discipline, contract.school_year, alternating, contract.get_period_display(),
            contract.rp.get_full_name(), contract.recruitment_type.label, contract.get_professional_expertise_level_display()
        ])
    xls = request.GET.get('xls')
    return export_csv('demandes_de_contrat', data, True if xls else False)


def speakers_list(request):
    speakers = Speaker.objects.all()
    form = SpeakerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            f"L'intervenant {form.cleaned_data['first_name']} {form.cleaned_data['last_name']} a bien été créé"
        )
    return render(request, 'nifleur/speakers.html', {
        'speakers': speakers,
        'form': form
    })


def speaker_details(request, speaker_id):
    speaker = get_object_or_404(Speaker, id=speaker_id)
    return render(request, 'nifleur/speaker_details.html', {'speaker': speaker})


def discipline_list(request):
    disciplines = Discipline.objects.all()
    form = DisciplineForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            f"La matière {form.cleaned_data['label']} a bien été créée pour la classe {form.cleaned_data['school_year']}"
        )
    return render(request, 'nifleur/disciplines.html', {
        'disciplines': disciplines,
        'form': form
    })


def school_details(request, school_id):
    school = get_object_or_404(StructureCampus, id=school_id)
    return render(request, 'nifleur/school_details.html', {'school': school})
