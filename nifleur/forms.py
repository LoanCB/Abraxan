from django import forms

from nifleur.models import Discipline, Speaker


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
