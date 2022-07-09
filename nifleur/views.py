import codecs
import csv

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from nifleur.forms import DisciplineForm, SpeakerForm, ContractRequestForm, PerformanceForm, SchoolYearForm, \
    SchoolForm, RecruitmentTypeForm, RateTypeForm, CompanyTypeForm, UnitForm, RegisterForm
from nifleur.models import ContractRequest, Speaker, Discipline, School, Performance, SchoolYear, Status, \
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


def import_data(request, file, model, status=False):
    django_model = apps.get_model(app_label='nifleur', model_name=model)
    csv_reader = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=';')
    for row in csv_reader:
        try:
            if status:
                django_model.objects.create(label=row[0], position=row[1])
            else:
                django_model.objects.create(label=row[0])
        except IntegrityError as e:
            if request.user.is_superuser:
                messages.error(request, e)
            else:
                messages.error(request, f"La donnée nomée {row[0]} existe déjà")
    return messages.info(request, f"Des données on été importées")


def parameters(request):
    # models data
    performances = Performance.objects.all().order_by('label')
    school_years = SchoolYear.objects.all()
    status = Status.objects.all().order_by('position')
    schools = School.objects.all()
    recruitment_types = RecruitmentType.objects.all()
    rate_types = RateType.objects.all()
    company_types = CompanyType.objects.all()
    units = Unit.objects.all()
    users = User.objects.all()

    # Forms
    performance_form = PerformanceForm(request.POST or None, prefix='performance-form')
    school_year_form = SchoolYearForm(request.POST or None, prefix='shcool_year-form')
    school_form = SchoolForm(request.POST or None, prefix='school-form')
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

    if request.method == 'POST':
        try:
            performance_csv = request.FILES['performance_csv']
        except MultiValueDictKeyError:
            performance_csv = None

        try:
            recruitment_type_csv = request.FILES['recruitment_type_csv']
        except MultiValueDictKeyError:
            recruitment_type_csv = None

        try:
            rate_type_csv = request.FILES['rate_type_csv']
        except MultiValueDictKeyError:
            rate_type_csv = None

        try:
            company_type_csv = request.FILES['company_type_csv']
        except MultiValueDictKeyError:
            company_type_csv = None

        try:
            unit_csv = request.FILES['unit_csv']
        except MultiValueDictKeyError:
            unit_csv = None

        try:
            status_csv = request.FILES['status_csv']
        except MultiValueDictKeyError:
            status_csv = None

        if performance_csv:
            import_data(request, performance_csv, 'Performance')
        elif recruitment_type_csv:
            import_data(request, recruitment_type_csv, 'RecruitmentType')
        elif rate_type_csv:
            import_data(request, rate_type_csv, 'RateType')
        elif company_type_csv:
            import_data(request, company_type_csv, 'CompanyType')
        elif unit_csv:
            import_data(request, unit_csv, 'Unit')
        elif status_csv:
            import_data(request, status_csv, 'Status', True)

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
        contract_request = form.save()
        messages.success(request, "La demande de contrat a bien été créée")
        return redirect(contract_request_detail, contract_request.id)
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
            short_datetime(contract.created_at), contract.school.label, contract.speaker.get_civility_display(),
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
    campus = School.objects.filter(structure_school_year__disciplines__speaker=speaker)
    data = dict()

    for school in campus.all():
        if school in data:
            data[school] += 1
        else:
            data[school] = 1
    morris_data = [({'label': m_data.label, 'value': data[m_data]}) for m_data in data]

    speaker_hours = 0
    for contract in speaker.contract_request_speaker.all():
        speaker_hours += contract.hourly_volume

    return render(request, 'nifleur/speaker_details.html', {
        'speaker': speaker,
        'morris_data': morris_data,
        'speaker_hours': speaker_hours
    })


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
    school = get_object_or_404(School, id=school_id)
    return render(request, 'nifleur/school_details.html', {'school': school})
