from django import forms

from nifleur.models import Discipline, Speaker, ContractRequest, Performance, SchoolYear, Status, StructureCampus, \
    RecruitmentType, RateType, CompanyType, Unit


class CustomModelForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class DisciplineForm(CustomModelForm):
    required_css_class = 'required'

    class Meta:
        model = Discipline
        fields = ['school_year', 'label', 'speaker']

    def __init__(self, *args, **kwargs):
        super(DisciplineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SpeakerForm(CustomModelForm):
    class Meta:
        model = Speaker
        fields = [
            'first_name', 'last_name', 'civility', 'mail', 'phone_number', 'highest_degree',
            'main_area_of_expertise', 'second_area_of_expertise', 'third_area_of_expertise', 'teaching_expertise_level'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '0_ __ __ __ __', 'data-slots': '_'})
        }


class ContractRequestForm(CustomModelForm):
    class Meta:
        model = ContractRequest
        fields = [
            'structure_campus', 'speaker', 'comment', 'status', 'performance', 'applied_rate', 'rate_type', 'ttc',
            'hourly_volume', 'unit', 'started_at', 'ended_at', 'discipline', 'school_year', 'alternating', 'period',
            'rp', 'recruitment_type', 'professional_expertise_level'
        ]

    def __init__(self, *args, **kwargs):
        super(ContractRequestForm, self).__init__(*args, **kwargs)
        self.fields['ttc'].widget.attrs['class'] = 'form-check-input'
        self.fields['alternating'].widget.attrs['class'] = 'form-check-input'


class PerformanceForm(CustomModelForm):
    class Meta:
        model = Performance
        fields = ['label']


class SchoolYearForm(CustomModelForm):
    class Meta:
        model = SchoolYear
        fields = ['structure_campus', 'year', 'label']


class StatusForm(CustomModelForm):
    class Meta:
        model = Status
        fields = ['position', 'label']


class StructureCampusForm(CustomModelForm):
    class Meta:
        model = StructureCampus
        fields = ['label', 'full_name']


class RecruitmentTypeForm(CustomModelForm):
    class Meta:
        model = RecruitmentType
        fields = ['label']


class RateTypeForm(CustomModelForm):
    class Meta:
        model = RateType
        fields = ['label']


class CompanyTypeForm(CustomModelForm):
    class Meta:
        model = CompanyType
        fields = ['label']


class UnitForm(CustomModelForm):
    class Meta:
        model = Unit
        fields = ['label']
