from django.contrib import admin

from nifleur.models import StructureCampus, CompanyType, Company, Speaker, Performance, RateType, SchoolYear, \
    Discipline, Status, Unit, RecruitmentType, ContractRequest


@admin.register(StructureCampus)
class StructureCampusAdmin(admin.ModelAdmin):
    list_display = ('label', 'full_name')


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('label', 'company_type', 'relation_mail', 'relation_phone_number')


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'civility', 'company', 'mail', 'phone_number', 'highest_degree',
        'main_area_of_expertise', 'second_area_of_expertise', 'third_area_of_expertise',
        'teaching_expertise_level'
    )


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(RateType)
class RateTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ('structure_campus', 'year', 'label')


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('school_year', 'label', 'speaker')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('position', 'label')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(RecruitmentType)
class RecruitmentTypeAdmin(admin.ModelAdmin):
    list_display = ('label',)


@admin.register(ContractRequest)
class ContractRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'structure_campus', 'speaker', 'created_at', 'comment', 'status', 'performance', 'applied_rate',
        'rate_type', 'ttc', 'hourly_volume', 'unit', 'started_at', 'ended_at', 'discipline', 'school_year',
        'alternating', 'period', 'rp', 'recruitment_type', 'professional_expertise_level'
    )
