from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from nifleur.forms import DisciplineForm, SpeakerForm, ContractRequestForm, PerformanceForm, SchoolYearForm, \
    StructureCampusForm, RecruitmentTypeForm, RateTypeForm, CompanyTypeForm, UnitForm, RegisterForm
from nifleur.models import ContractRequest, Speaker, Discipline, StructureCampus, Performance, SchoolYear, Status, \
    RecruitmentType, RateType, CompanyType, Unit
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


def parameters(request):
    # models data
    performances = Performance.objects.all().order_by('label')
    school_years = SchoolYear.objects.all()
    status = Status.objects.all()
    schools = StructureCampus.objects.all()
    recruitment_types = RecruitmentType.objects.all()
    rate_types = RateType.objects.all()
    company_types = CompanyType.objects.all()
    units = Unit.objects.all()
    users = User.objects.all()

    # Forms
    performance_form = PerformanceForm(request.POST or None, prefix='performance-form')
    school_year_form = SchoolYearForm(request.POST or None, prefix='shcool_year-form')
    school_form = StructureCampusForm(request.POST or None, prefix='school-form')
    recruitment_type_form = RecruitmentTypeForm(request.POST or None, prefix='recruitment_typ-form')
    rate_type_form = RateTypeForm(request.POST or None, prefix='rate_type-form')
    company_type_form = CompanyTypeForm(request.POST or None, prefix='company_type-form')
    unit_form = UnitForm(request.POST or None, prefix='unit-form')
    user_form = RegisterForm(request.POST or None, prefix='user-form')

    if performance_form.is_valid():
        performance_form.save()
        messages.success(request, "Une nouvelle performance a bien été créée")
        return redirect(parameters)

    if school_year_form.is_valid():
        school_year_form.save()
        messages.success(request, "Une nouvelle promotion a bien été créée")
        return redirect(parameters)

    if school_form.is_valid():
        school_form.save()
        messages.success(request, "Une nouvelle école a bien été créée")
        return redirect(parameters)

    if recruitment_type_form.is_valid():
        recruitment_type_form.save()
        messages.success(request, "Un nouveau type de recrutement a bien été créé")
        return redirect(parameters)

    if rate_type_form.is_valid():
        rate_type_form.save()
        messages.success(request, "Un nouveau type de tarif a bien été créé")
        return redirect(parameters)

    if company_type_form.is_valid():
        company_type_form.save()
        messages.success(request, "Un nouveau type de société a bien été créé")
        return redirect(parameters)

    if unit_form.is_valid():
        unit_form.save()
        messages.success(request, "Une nouvelle unité a bien été créée")
        return redirect(parameters)

    if user_form.is_valid():
        user_form.save()
        messages.success(request, "Une nouvel utilisateur a bien été créé")
        return redirect(parameters)

    return render(request, 'nifleur/parameters.html', {
        'performances': performances,
        'school_years': school_years,
        'status': status,
        'schools': schools,
        'recruitment_types': recruitment_types,
        'rate_types': rate_types,
        'company_types': company_types,
        'units': units,
        'users': users,
        'performance_form': performance_form,
        'school_year_form': school_year_form,
        'school_form': school_form,
        'recruitment_type_form': recruitment_type_form,
        'rate_type_form': rate_type_form,
        'company_type_form': company_type_form,
        'unit_form': unit_form,
        'user_form': user_form
    })


def delete_model_object(request, model, object_id):
    django_model = apps.get_model(app_label='nifleur', model_name=model)
    model_object = get_object_or_404(django_model, id=object_id)
    model_object.delete()
    return JsonResponse({'success': True})


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
    data = [[
        'Date Demande', 'Marque / Ecole', 'Civilité', 'Nom', 'Prénom', 'Type société', 'Société', 'Commentaire',
        'Status contrat', 'Type de mission', 'Tarif a appliquer', 'TTC/SST', 'Horaire ou forfait', 'Volume horaire',
        'Unité', 'Date début', 'Date fin', 'Matière', 'Promotion', 'Alternant/Initial', 'Période', 'RP', 'Téléphone',
        'Mail', 'Type de recrutement', 'Intitulé du diplôme le plus élevé', 'Domaine de compétence principal',
        'Domaine de compétence 2', 'Domaine de compétence 3', "Niveau d'expertise en pédagogie",
        "Niveau d'expertise matière professionnelle"
    ]]
    for contract in contract_requests:
        ttc = 'TTC' if contract.ttc else 'SST'
        alternating = 'Alternant' if contract.alternating else 'Initial'
        if contract.speaker.company:
            company = contract.speaker.company.label
            company_type = contract.speaker.company.company_type
        else:
            company = ''
            company_type = ''
        data.append([
            short_datetime(contract.created_at), contract.structure_campus.label, contract.speaker.get_civility_display(),
            contract.speaker.last_name, contract.speaker.first_name, company_type, company, contract.comment,
            contract.status.label, contract.performance.label, contract.applied_rate, ttc, contract.rate_type.label,
            contract.hourly_volume, contract.unit.label, short_datetime(contract.started_at),
            short_datetime(contract.ended_at), contract.discipline.label, contract.school_year.year, alternating,
            contract.get_period_display(), contract.rp.get_full_name(), contract.speaker.phone_number,
            contract.speaker.mail, contract.recruitment_type.label, contract.speaker.highest_degree,
            contract.speaker.main_area_of_expertise, contract.speaker.second_area_of_expertise,
            contract.speaker.third_area_of_expertise, contract.speaker.get_teaching_expertise_level_display(),
            contract.get_professional_expertise_level_display()
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
    disciplines = Discipline.objects.all().order_by('school_year')
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
