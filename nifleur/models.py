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
    A company have a type

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Type de la compagnie'
        verbose_name_plural = 'Types des compagnies'

    def __str__(self):
        return self.label

    @property
    def get_verbose_name(self):
        return 'un type de société'


class Company(models.Model):
    """
    A speaker can have a company

    Attributes:

    - :class:`str` label
    - :class:`CompanyType` company_type
    - :class:`str` relation_mail
    - :class:`str` relation_phone_number
    """
    label = models.CharField('Nom', max_length=255, unique=True)
    company_type = models.ForeignKey(
        CompanyType,
        verbose_name='Type de la compagnie',
        related_name='speaker_company_type',
        on_delete=models.PROTECT,
        null=True,
        blank=True
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
    - :class:`int` professional_expertise_level
    """
    MEN = 'M'
    WOMEN = 'W'
    CIVILITY = (
        (MEN, 'M.'),
        (WOMEN, 'Mme')
    )
    first_name = models.CharField('Prénom', max_length=50)
    last_name = models.CharField('Nom', max_length=100)
    civility = models.CharField('Civilité', max_length=1, choices=CIVILITY, default=MEN)
    company = models.ForeignKey(
        Company,
        verbose_name='Société',
        related_name='speaker_company',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    mail = models.EmailField(unique=True)
    phone_number = PhoneNumberField(verbose_name='Numéro de téléphone', null=True, blank=True)
    highest_degree = models.CharField('Diplôme le plus élevé', max_length=255, null=True)
    main_area_of_expertise = models.CharField('Domaine de compétence principal', max_length=255, null=True)
    second_area_of_expertise = models.CharField(
        'Deuxième domaine de compétence',
        max_length=255,
        null=True,
        blank=True
    )
    third_area_of_expertise = models.CharField('Troisième domaine de compétence', max_length=255, null=True, blank=True)
    teaching_expertise_level = models.PositiveSmallIntegerField(
        "Niveau d'expertise en pédagogie",
        choices=LEVELS,
        null=True
    )
    professional_expertise_level = models.PositiveSmallIntegerField(
        "Niveau d'expertise en matière professionnelle",
        choices=LEVELS,
        null=True
    )

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

    @property
    def get_verbose_name(self):
        return 'une prestation'


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

    @property
    def get_verbose_name(self):
        return 'un type de tarif'


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
    - :class:`School` school
    - :class:`str` label
    - :class:`Speaker` speaker
    """
    school_year = models.ForeignKey(
        SchoolYear,
        verbose_name='Classe',
        related_name='disciplines',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    school = models.ForeignKey(
        School,
        verbose_name='Ecole',
        related_name='disciplines',
        on_delete=models.PROTECT
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

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'

    def __str__(self):
        return self.label

    def clean(self, *args, **kwargs):
        if not self.school and self.school_year:
            self.school = self.school_year.school
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


OPEN = 1
ON_GOING = 2
CLOSE = 3
STATUS_CHOICES = (
    (OPEN, 'ouvert'),
    (ON_GOING, 'en cours'),
    (CLOSE, 'fermé')
)


class Status(models.Model):
    """
    A status is required for a contract request

    Attributes:

    - :class:`int` position
    - :class:`str` label
    - :class:`str` color
    - :class:`int` type
    """
    position = models.PositiveSmallIntegerField('position')
    label = models.CharField('Nom', max_length=50, unique=True)
    color = models.CharField(
        'couleur',
        max_length=9,
        unique=True,
        help_text="Couleur hexadécimale du status (avec le #)"
    )
    type = models.PositiveSmallIntegerField('type', choices=STATUS_CHOICES, default=OPEN)

    class Meta:
        verbose_name = 'Statut'
        verbose_name_plural = 'Statuts'

    def __str__(self):
        return f'{self.position} - {self.label}'

    @property
    def get_verbose_name(self):
        return 'un statut'

    @property
    def can_back(self):
        return self.position > 1

    @property
    def can_next(self):
        # FIXME Potential bug if position not in strict order
        return self.position < Status.objects.count()

    @property
    def finish(self):
        return self == Status.objects.filter(type=CLOSE).first()

    @property
    def cancel(self):
        # FIXME Potential bug if new status CLOSE was created
        return self == Status.objects.filter(type=CLOSE).last()


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

    @property
    def get_verbose_name(self):
        return 'une unité'


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

    @property
    def get_verbose_name(self):
        return 'un  type de recrutement'


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

    @property
    def get_verbose_name(self):
        return 'une structure juridique'


class ContractRequest(TimeStampedModel):
    """
    Main model to list all contract requests

    Attributes:

    - :class:`School` school
    - :class:`LegalStructure` legal_structure
    - :class:`Speaker` speaker
    - :class:`Company` company
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
    - :class:`User` rp
    - :class:`int` recruitment_type
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
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    comment = models.CharField('Commentaire', max_length=255, null=True, blank=True)
    status = models.ForeignKey(
        Status,
        verbose_name='Statut',
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
        verbose_name="Horaire ou forfait",
        related_name='contract_request_rate',
        on_delete=models.PROTECT
    )
    ttc = models.BooleanField('TVA', help_text='SST si faux', default=False)
    hourly_volume = models.FloatField('Volume horaire')
    unit = models.ForeignKey(
        Unit,
        verbose_name='Unité',
        related_name='contract_request_unit',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
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
    period = models.CharField('Période', choices=PERIOD, max_length=2)
    rp = models.ForeignKey(User, verbose_name='Responsable pédagogique', related_name='rp', on_delete=models.PROTECT)
    recruitment_type = models.ForeignKey(
        RecruitmentType,
        verbose_name='Type de recrutement',
        related_name='contract_request_recrutement_type',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Demande de contrat'
        verbose_name_plural = 'Demandes de contrat'

    def __str__(self):
        return f"Demande de contrat de {self.speaker.get_civility_display()} {self.speaker}"

    def get_absolute_url(self):
        return reverse('contract_request_detail', kwargs={'contract_id': self.id})
