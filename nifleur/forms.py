from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from nifleur.models import Discipline, Speaker, ContractRequest, Performance, SchoolYear, Status, School, \
    RecruitmentType, RateType, CompanyType, Unit, LegalStructure


class CustomModelForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DisciplineForm(CustomModelForm):
    class Meta:
        model = Discipline
        fields = ['school_year', 'label', 'speaker']


class SpeakerForm(CustomModelForm):
    class Meta:
        model = Speaker
        fields = (
            'first_name', 'last_name', 'civility', 'mail', 'phone_number', 'highest_degree',
            'main_area_of_expertise', 'second_area_of_expertise', 'third_area_of_expertise', 'teaching_expertise_level'
        )
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '0_ __ __ __ __', 'data-slots': '_'})
        }


class ContractRequestForm(CustomModelForm):
    class Meta:
        model = ContractRequest
        fields = (
            'school', 'legal_structure', 'speaker', 'comment', 'status', 'performance', 'applied_rate', 'rate_type',
            'ttc', 'hourly_volume', 'unit', 'started_at', 'ended_at', 'discipline', 'school_year', 'rp',
            'recruitment_type', 'professional_expertise_level'
        )

    def __init__(self, *args, **kwargs):
        super(ContractRequestForm, self).__init__(*args, **kwargs)
        self.fields['ttc'].widget.attrs['class'] = 'form-check-input'
        self.fields['started_at'].widget.attrs['class'] += ' datepicker_input'
        self.fields['ended_at'].widget.attrs['class'] += ' datepicker_input'


class PerformanceForm(CustomModelForm):
    class Meta:
        model = Performance
        fields = ('label',)


class SchoolYearForm(CustomModelForm):
    class Meta:
        model = SchoolYear
        fields = ('school', 'year', 'label', 'initial', 'alternating')

    def __init__(self, *args, **kwargs):
        super(SchoolYearForm, self).__init__(*args, **kwargs)
        self.fields['initial'].widget.attrs['class'] = 'form-check-input'
        self.fields['alternating'].widget.attrs['class'] = 'form-check-input'


class SchoolYearDetailForm(CustomModelForm):
    class Meta:
        model = SchoolYear
        fields = ('year', 'label', 'initial', 'alternating')

    def __init__(self, *args, **kwargs):
        super(SchoolYearDetailForm, self).__init__(*args, **kwargs)
        self.fields['initial'].widget.attrs['class'] = 'form-check-input'
        self.fields['alternating'].widget.attrs['class'] = 'form-check-input'


class SchoolForm(CustomModelForm):
    class Meta:
        model = School
        fields = ('label', 'full_name')


class RecruitmentTypeForm(CustomModelForm):
    class Meta:
        model = RecruitmentType
        fields = ('label',)


class RateTypeForm(CustomModelForm):
    class Meta:
        model = RateType
        fields = ('label',)


class CompanyTypeForm(CustomModelForm):
    class Meta:
        model = CompanyType
        fields = ('label',)


class UnitForm(CustomModelForm):
    class Meta:
        model = Unit
        fields = ('label',)


class LegalStructureForm(CustomModelForm):
    class Meta:
        model = LegalStructure
        fields = ('label',)


class RegisterForm(CustomModelForm, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'is_staff')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['is_staff'].widget.attrs['class'] = 'form-check-input'

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
