from django.contrib import admin

# Register your models here.
from nifleur.models import ContractRequest, StructureCampus, Speaker, Performance, RateType, Discipline, SchoolYear


@admin.register(ContractRequest)
class ContractRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'structure_campus', 'speaker', 'created_at', 'comment', 'status', 'performance', 'applied_rate',
        'rate_type', 'ttc', 'hourly_volume', 'unit', 'started_at', 'ended_at', 'discipline', 'school_year',
        'alternating', 'period', 'rp', 'recruitment_type', 'highest_degree', 'teaching_expertise_level',
        'professional_expertise_level'
    )


@admin.register(StructureCampus)
class StructureCampusAdmin(admin.ModelAdmin):
    list_display = ('label', 'full_name')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'civility', 'company_type', 'mail', 'phone_number',
        'main_area_of_expertise', 'second_area_of_expertise', 'third_area_of_expertise')


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(RateType)
class RateTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('school_year', 'label', 'speaker')


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('structure_campus', 'year', 'label')
