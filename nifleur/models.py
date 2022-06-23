from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3
LEVELS = (
    (BEGINNER, 'Débutant'),
    (INTERMEDIATE, 'Intermédiaire'),
    (EXPERT, 'Expert')
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


class StructureCampus(models.Model):
    """
    Value of structure or campus

    Attributes:

    - :class:`str` label -> Name of the campus or structure
    - :class:`str` full_name -> Full name of the campus or structure
    """
    label = models.CharField('Nom', max_length=20)
    full_name = models.CharField('Nom complet', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Structure & campus'
        verbose_name_plural = 'Structures & campus'

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('school_details', kwargs={'school_id': self.id})


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
    """
    MEN = 'M'
    WOMEN = 'W'
    CIVILITY = (
        (MEN, 'Mr'),
        (WOMEN, 'Mme')
    )
    MICRO_ENTERPRISE = 1
    SOCIETY = 2
    PROFESSION = 3
    WAGE_PORTAGE = 4
    COMPANIES_TYPE = (
        (MICRO_ENTERPRISE, 'Micro-entreprise'),
        (SOCIETY, 'société'),
        (PROFESSION, 'Profession libérale'),
        (WAGE_PORTAGE, 'Portage salariale')
    )
    first_name = models.CharField('Prénom', max_length=50)
    last_name = models.CharField('Nom', max_length=100)
    civility = models.CharField('Civilité', max_length=1, choices=CIVILITY, default=MEN)
    company_type = models.PositiveSmallIntegerField('Type de la société', choices=COMPANIES_TYPE, blank=True, null=True)
    company = models.CharField('société', max_length=255, blank=True, null=True)
    mail = models.EmailField()
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


class Performance(models.Model):
    """
    A contract request reattached to a performance

    Attributes:

    - :class:`str` label
    """
    label = models.CharField('Nom', max_length=255)

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
    label = models.CharField('Nom', max_length=255)

    class Meta:
        verbose_name = 'Type de tarif'
        verbose_name_plural = 'Types de tarif'

    def __str__(self):
        return self.label


class SchoolYear(models.Model):
    """
    A school year reattached to a structure campus. A contract request need a school year

    Attributes:

    - :class:`StructureCampus` structure_campus
    - :class:`str` year -> Year of the school year (ex: M1, L2, B3...)
    - :class:`str` label
    """
    structure_campus = models.ForeignKey(
        StructureCampus,
        verbose_name='Ecole',
        related_name='structure_school_year',
        on_delete=models.PROTECT
    )
    year = models.CharField('Année', max_length=15, help_text='ex: M1')
    label = models.CharField('Nom', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        if self.label:
            return f'{self.structure_campus} - {self.year} - {self.label}'
        return f'{self.structure_campus} - {self.year}'


class Discipline(models.Model):
    """
    A contract request reattached to a discipline

    Attributes:

    - :class:`SchoolYear` school_year
    - :class:`str` label
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

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'

    def __str__(self):
        return self.label


class ContractRequest(TimeStampedModel):
    """
    Main model to list all contract requests

    Attributes:

    - :class:`StructureCampus` structure_campus
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
    RH_DURING = 1
    RH_TODO = 2
    TO_DO = 3
    WAITING_DOC = 4
    GP_GAP = 5
    INCOMPLETE_REQUEST = 6
    DONE = 7
    SEND = 8
    SIGN = 9
    SECOND_PERIOD = 10
    CANCEL = 11
    STATUS = (
        (RH_DURING, 'RH en cours de traitement'),
        (RH_TODO, 'RH dossier complet - à traiter'),
        (TO_DO, 'Dossier complet - à faire'),
        (WAITING_DOC, 'Attente de document'),
        (GP_GAP, 'écart GP'),
        (INCOMPLETE_REQUEST, 'Demande incomplète'),
        (DONE, 'Fait'),
        (SEND, 'Envoyé'),
        (SIGN, 'Signé'),
        (SECOND_PERIOD, 'Deuxième période'),
        (CANCEL, 'Annulé')
    )

    HALF_DAY = 1
    DAY = 2
    FLAT_FEE = 3
    HOUR = 4
    OTHER = 5
    UNIT = (
        (HALF_DAY, 'demies-journées'),
        (DAY, 'journées'),
        (FLAT_FEE, 'forfaits'),
        (HOUR, 'heures'),
        (OTHER, 'autre')
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

    RECRUITMENT = 1
    RENEWAL = 2
    ADD_SERVICE = 3
    RECRUITMENT_TYPE = (
        (RECRUITMENT, 'Recrutement'),
        (RENEWAL, 'Reconduction'),
        (ADD_SERVICE, 'Ajout de prestation'),
    )

    structure_campus = models.ForeignKey(
        StructureCampus,
        verbose_name='Structure ou campus',
        related_name='contract_request_structure',
        on_delete=models.PROTECT
    )
    speaker = models.ForeignKey(
        Speaker,
        verbose_name='Intervenant',
        related_name='contract_request_speaker',
        on_delete=models.PROTECT
    )
    comment = models.CharField('Commentaire', max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField('Statut', choices=STATUS, default=WAITING_DOC)
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
    unit = models.PositiveSmallIntegerField('Unité', choices=UNIT)
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
    alternating = models.BooleanField('Alternant', help_text="Est une classe d'alternants", default=False)
    period = models.CharField('Période', choices=PERIOD, max_length=2)
    rp = models.ForeignKey(User, verbose_name='Responsable pédagogique', related_name='rp', on_delete=models.PROTECT)
    recruitment_type = models.PositiveSmallIntegerField('Type de recrutement', choices=RECRUITMENT_TYPE)
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
