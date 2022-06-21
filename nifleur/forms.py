from django.forms import ModelForm

from nifleur.models import Discipline


class DisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = ['school_year', 'label', 'speaker']
