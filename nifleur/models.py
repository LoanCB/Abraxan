from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3
LEVELS = (
    (BEGINNER, 'Débutant'),
    (INTERMEDIATE, 'Intermédiaire'),
    (EXPERT, 'Expert')
)

SEMESTER_1 = 'S1'
SEMESTER_2 = 'S2'
QUARTER_1 = 'Q1'
QUARTER_2 = 'Q2'
QUARTER_3 = 'Q3'
PERIOD = (
    (SEMESTER_1, 'Semestre 1'),
    (SEMESTER_2, 'Semestre 2'),
    (QUARTER_1, 'Trimestre 1'),
    (QUARTER_2, 'Trimestre 2'),
    (QUARTER_3, 'Trimestre 3')
)


class TimeStampedModel(models.Model):
    """
    Abstract base model to have automatic fields for creation and update

    Attributes:

    - :class:`datetime` created_at --> Date and time when the instance was created
    - :class:`datetime` updated_at --> Date and time when the instance was last edited
    """
    created_at = models.DateTimeField('date de création', auto_now_add=True)
    updated_at = models.DateTimeField('date de dernière modification', auto_now=True)

    class Meta:
        abstract = True


class School(models.Model):
    """
    Value of school

    Attributes:

    - :class:`str` label -> Name of the school
    - :class:`str` full_name -> Full name of the school
    """
    label = models.CharField('Nom', max_length=20, unique=True)
    full_name = models.CharField('Nom complet', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Ecole'
        verbose_name_plural = 'Ecoles'

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('school_details', kwargs={'school_id': self.id})


class CompanyType(models.Model):
    """

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Type de la compagnie'
        verbose_name_plural = 'Types des compagnies'

    def __str__(self):
        return self.label


class Company(models.Model):
    """

    """
    label = models.CharField('Nom', max_length=255, unique=True)
    company_type = models.ForeignKey(
        CompanyType,
        verbose_name='Type de la compagnie',
        related_name='speaker_company_type',
        on_delete=models.PROTECT
    )
    relation_mail = models.EmailField(verbose_name='mail de la relation', null=True, blank=True, unique=True)
    relation_phone_number = PhoneNumberField(
        verbose_name='Numéro de téléphone de la relation',
        null=True,
        blank=True,
        unique=True
    )

    class Meta:
        verbose_name = 'Société'
        verbose_name_plural = 'Sociétés'

    def __str__(self):
        return f"{self.label} ({self.company_type})"


class Speaker(models.Model):
    """
    A speaker belong to a contract request

    Attributes:

    - :class:`str` first_name
    - :class:`str` last_name
    - :class:`str` civility
    - :class:`str` company_type
    - :class:`str` mail
    - :class:`str` phone_number
    - :class:`str` main_area_of_expertise
    - :class:`str` second_area_of_expertise
    - :class:`str` third_area_of_expertise
    - :class:`int` teaching_expertise_level
    """
    MEN = 'M'
    WOMEN = 'W'
    CIVILITY = (
        (MEN, 'Mr'),
        (WOMEN, 'Mme')
    )
    first_name = models.CharField('Prénom', max_length=50)
    last_name = models.CharField('Nom', max_length=100)
    civility = models.CharField('Civilité', max_length=1, choices=CIVILITY, default=MEN)
    company = models.ForeignKey(
        Company,
        verbose_name='Compagnie',
        related_name='speaker_company',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    mail = models.EmailField(unique=True)
    phone_number = PhoneNumberField(verbose_name='Numéro de téléphone', null=True, blank=True)
    highest_degree = models.CharField('Diplôme le plus élevé', max_length=255)
    main_area_of_expertise = models.CharField('Domaine de compétence principal', max_length=255)
    second_area_of_expertise = models.CharField(
        'Deuximème domaine de compétence',
        max_length=255,
        null=True,
        blank=True
    )
    third_area_of_expertise = models.CharField('Troisième domaine de compétence', max_length=255, null=True, blank=True)
    teaching_expertise_level = models.PositiveSmallIntegerField("Niveau d'expertise en pédagogie", choices=LEVELS)

    class Meta:
        verbose_name = 'Intervenant'
        verbose_name_plural = 'Intervenants'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('speaker_details', kwargs={'speaker_id': self.id})

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Performance(models.Model):
    """
    A contract request reattached to a performance

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Prestation'
        verbose_name_plural = 'Prestations'

    def __str__(self):
        return self.label


class RateType(models.Model):
    """
    A contract request reattached to a rate type

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Type de tarif'
        verbose_name_plural = 'Types de tarif'

    def __str__(self):
        return self.label


class SchoolYear(models.Model):
    """
    A school year reattached to a school. A contract request need a school year

    Attributes:

    - :class:`School` school
    - :class:`str` year -> Year of the school year (ex: M1, L2, B3...)
    - :class:`str` label
    - :class:`bool` initial
    - :class:`bool` alternating
    """
    school = models.ForeignKey(
        School,
        verbose_name='Ecole',
        related_name='school_year',
        on_delete=models.PROTECT
    )
    year = models.CharField('Année', max_length=15, help_text='ex: M1')
    label = models.CharField('Nom', max_length=255, blank=True, null=True)
    initial = models.BooleanField('Initiale', default=False, help_text="Est une classe avec des élèves en initial")
    alternating = models.BooleanField(
        'Alternant',
        default=False,
        help_text="Est une classe avec des élèves en alternance"
    )

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        if self.label:
            return f'{self.school} - {self.year} - {self.label}'
        return f'{self.school} - {self.year}'

    def clean(self, *args, **kwargs):
        if not self.initial and not self.alternating:
            raise ValidationError(
                _("Une classe doit possède au moins des initiaux ou des alternants ou les deux"),
                code='invalid'
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Discipline(models.Model):
    """
    A contract request reattached to a discipline

    Attributes:

    - :class:`SchoolYear` school_year
    - :class:`str` label
    - :class:`Speaker` speaker
    - :class:`str` period
    """
    school_year = models.ForeignKey(
        SchoolYear,
        verbose_name='Classe',
        related_name='disciplines',
        on_delete=models.PROTECT,
        null=True
    )
    label = models.CharField('Nom', max_length=255)
    speaker = models.ForeignKey(
        Speaker,
        verbose_name='Intervenant',
        related_name='discipline',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    period = models.CharField('Période', choices=PERIOD, max_length=2)

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'

    def __str__(self):
        return self.label


class Status(models.Model):
    """
    A status is required for a contract request

    Attributes:

    - :class:`int` position
    - :class:`str` label
    """
    position = models.PositiveSmallIntegerField('position')
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Statut'
        verbose_name_plural = 'Statuts'

    def __str__(self):
        return f'{self.position} - {self.label}'


class Unit(models.Model):
    """

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Unité'
        verbose_name_plural = 'Unités'

    def __str__(self):
        return self.label


class RecruitmentType(models.Model):
    """

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Type de recrutement'
        verbose_name_plural = 'Types de recrutement'

    def __str__(self):
        return self.label


class LegalStructure(models.Model):
    """
    A legal structure is required for a contract request

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Structure juridique'
        verbose_name_plural = 'Structures juridique'

    def __str__(self):
        return self.label


class ContractRequest(TimeStampedModel):
    """
    Main model to list all contract requests

    Attributes:

    - :class:`School` school
    - :class:`LegalStructure` legal_structure
    - :class:`Speaker` speaker
    - :class:`str` comment
    - :class:`int` status
    - :class:`Performance` performance
    - :class:`float` applied_rate
    - :class:`RateType` rate_type
    - :class:`bool` ttc
    - :class:`float` hourly_volume
    - :class:`int` unit
    - :class:`datetime` started_at
    - :class:`datetime` ended_at
    - :class:`Discipline` discipline
    - :class:`SchoolYear` school_year
    - :class:`bool` alternating
    - :class:`str` period
    - :class:`User` rp
    - :class:`int` recruitment_type
    - :class:`str` highest_degree
    - :class:`int` teaching_expertise_level
    - :class:`int` professional_expertise_level
    """
    school = models.ForeignKey(
        School,
        verbose_name='Ecole',
        related_name='contract_request_school',
        on_delete=models.PROTECT
    )
    legal_structure = models.ForeignKey(
        LegalStructure,
        verbose_name='Structure juridique',
        related_name='contract_request_structure',
        on_delete=models.PROTECT
    )
    speaker = models.ForeignKey(
        Speaker,
        verbose_name='Intervenant',
        related_name='contract_request_speaker',
        on_delete=models.PROTECT
    )
    company = models.ForeignKey(
        Company,
        verbose_name='Société',
        related_name='contract_request_company',
        on_delete=models.PROTECT
    )
    comment = models.CharField('Commentaire', max_length=255, null=True, blank=True)
    status = models.ForeignKey(
        Status,
        verbose_name='Status',
        related_name='contract_request_status',
        on_delete=models.PROTECT
    )
    performance = models.ForeignKey(
        Performance,
        verbose_name='Prestation',
        related_name='contract_request_performance',
        on_delete=models.PROTECT
    )
    applied_rate = models.FloatField('Tarif à appliquer')
    rate_type = models.ForeignKey(
        RateType,
        verbose_name="Type d'horaire",
        related_name='contract_request_rate',
        on_delete=models.PROTECT
    )
    ttc = models.BooleanField('Toute Taxes Comprises', help_text='SST si faux', default=False)
    hourly_volume = models.FloatField('Volume horaire')
    unit = models.ForeignKey(Unit, verbose_name='Unité', related_name='contract_request_unit', on_delete=models.PROTECT)
    started_at = models.DateTimeField('Début du contrat')
    ended_at = models.DateTimeField('Fin du contrat')
    discipline = models.ForeignKey(
        Discipline,
        verbose_name="Matière",
        related_name='contract_request_discipline',
        on_delete=models.PROTECT
    )
    school_year = models.ForeignKey(
        SchoolYear,
        verbose_name="Année de la promotion",
        related_name='contract_request_year',
        on_delete=models.PROTECT
    )
    rp = models.ForeignKey(User, verbose_name='Responsable pédagogique', related_name='rp', on_delete=models.PROTECT)
    recruitment_type = models.ForeignKey(
        RecruitmentType,
        verbose_name='Type de recrutement',
        related_name='contract_request_recrutement_type',
        on_delete=models.PROTECT
    )
    professional_expertise_level = models.PositiveSmallIntegerField(
        "Niveau d'expertise en matière professionnelle",
        choices=LEVELS
    )

    class Meta:
        verbose_name = 'Demande de contrat'
        verbose_name_plural = 'Demandes de contrat'

    def __str__(self):
        return f"Demande de contrat de {self.speaker.get_civility_display()}. {self.speaker}"

    def get_absolute_url(self):
        return reverse('contract_request_detail', kwargs={'contract_id': self.id})
