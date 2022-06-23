from django.forms import ModelForm

from nifleur.models import Discipline, Speaker


class DisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = ['school_year', 'label', 'speaker']


class SpeakerForm(ModelForm):
    class Meta:
        model = Speaker
        fields = [
            'first_name', 'last_name', 'civility', 'mail', 'phone_number', 'highest_degree',
            'main_area_of_expertise', 'second_area_of_expertise', 'third_area_of_expertise', 'teaching_expertise_level'
        ]
