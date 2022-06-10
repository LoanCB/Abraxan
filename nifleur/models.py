from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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


class ContractRequest(TimeStampedModel):
    """
    Main model to list all contract requests

    Attributes:

    - :class:`str` comment
    - :class:`int` status
    - :class:`float` applied_rate
    - :class:`bool` ttc
    - :class:`float` hourly_volume
    - :class:`int` unit
    - :class:`datetime` started_at
    - :class:`datetime` ended_at
    - :class:`bool` alternating
    - :class:`str` period
    - :class:`User` rp
    - :class:`int` recruitment_type
    - :class:`str` highest_degree
    - :class:`str` main_area_of_expertise
    - :class:`str` second_area_of_expertise
    - :class:`str` third_area_of_expertise
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
        (HALF_DAY, 'Demie-journée'),
        (DAY, 'Journée'),
        (FLAT_FEE, 'Forfait'),
        (HOUR, 'Heure'),
        (OTHER, 'Autre')
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

    BEGINNER = 1
    INTERMEDIATE = 2
    EXPERT = 3
    LEVELS = (
        (BEGINNER, 'Débutant'),
        (INTERMEDIATE, 'Intermédiaire'),
        (EXPERT, 'Expert')
    )

    comment = models.CharField('Commentaire', max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField('Statut', choices=STATUS, default=WAITING_DOC)
    applied_rate = models.FloatField('Tarif à appliquer')
    ttc = models.BooleanField('Toute Taxes Comprises', help_text='SST si faux', default=False)
    hourly_volume = models.FloatField('Volume horaire')
    unit = models.PositiveSmallIntegerField('Unité', choices=UNIT)
    started_at = models.DateTimeField('Début du contrat')
    ended_at = models.DateTimeField('Fin du contrat')
    alternating = models.BooleanField('Alternant', help_text="Est une classe d'alternants", default=False)
    period = models.CharField('Période', choices=PERIOD)
    rp = models.ForeignKey(User, verbose_name='Responsable pédagogique', related_name='rp', on_delete=models.PROTECT)
    recruitment_type = models.PositiveSmallIntegerField('Type de recrutement', choices=RECRUITMENT_TYPE)
    highest_degree = models.CharField('Diplôme le plus élevé', max_length=255)
    main_area_of_expertise = models.CharField('Domaine de compétence principal', max_length=255)
    second_area_of_expertise = models.CharField('Deuximèe domaine de compétence', max_length=255, null=True)
    third_area_of_expertise = models.CharField('Troisième domaine de compétence', max_length=255, blank=True)
    teaching_expertise_level = models.PositiveSmallIntegerField("Niveau d'expertise en pédagogie", choices=LEVELS)
    professional_expertise_level = models.PositiveSmallIntegerField(
        "Niveau d'expertise en matière professionnelle",
        choices=LEVELS
    )

    class Meta:
        verbose_name = 'Demande de contrat'
        verbose_name_plural = 'Demandes de contrat'

    def __str__(self):
        return f"Demande de contrat de {self.speaker.civility} {self.speaker}"

    # TODO get_absolute_url on ContractRequest model
    def get_absolute_url(self):
        pass


class StructureCampus(models.Model):
    """
    Value of structure or campus

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label -> Name of the campus or structure
    """
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Nom ou structure',
        related_name='structure_campus',
        on_delete=models.PROTECT
    )
    label = models.CharField('Nom', max_length=20)

    class Meta:
        verbose_name = 'Structure & campus'
        verbose_name_plural = 'Structures & campus'

    def __str__(self):
        return self.label


class Speaker(models.Model):
    """
    A speaker belong to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` first_name
    - :class:`str` last_name
    - :class:`str` civility
    - :class:`str` company_type
    - :class:`str` mail
    - :class:`str` phone_number
    """
    MEN = 'M'
    WOMEN = 'W'
    CIVILITY = (
        (MEN, 'Mr'),
        (WOMEN, 'Mme')
    )
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Intervenant',
        related_name='speaker',
        on_delete=models.PROTECT
    )
    first_name = models.CharField('Prénom', max_length=50)
    last_name = models.CharField('Nom', max_length=100)
    civility = models.CharField('Civilité', max_length=1, choices=CIVILITY, default=MEN)
    company_type = models.CharField('Type de la société', max_length=255, blank=True, null=True)
    mail = models.EmailField()
    phone_number = PhoneNumberField(verbose_name='Numéro de téléphone', null=True, blank=True)

    class Meta:
        verbose_name = 'Intervenant'
        verbose_name_plural = 'Intervenants'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # TODO get_absolute_url on Speaker model
    def get_absolute_url(self):
        pass


class Performance(models.Model):
    """
    A performance reattached to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label
    """
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Prestation',
        related_name='performance',
        on_delete=models.PROTECT
    )
    label = models.CharField('Nom', max_length=255)

    class Meta:
        verbose_name = 'Prestation'
        verbose_name_plural = 'Prestations'

    def __str__(self):
        return self.label


class RateType(models.Model):
    """
    A rate type reattached to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label
    """
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Type de tarif',
        related_name='rate_type',
        on_delete=models.PROTECT
    )
    label = models.CharField('Nom', max_length=255)

    class Meta:
        verbose_name = 'Type de tarif'
        verbose_name_plural = 'Types de tarif'

    def __str__(self):
        return self.label


class Discipline(models.Model):
    """
    A discipline reattached to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label
    """
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Matière',
        related_name='discipline',
        on_delete=models.PROTECT
    )
    label = models.CharField('Nom', max_length=255)

    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'

    def __str__(self):
        return self.label


class SchoolYear(models.Model):
    """
    A school year reattached to a structure campus and a contract request

    Attributes:

    - :class:`StructureCampus` structure_campus
    - :class:`ContractRequest` contract_request
    - :class:`str` year -> Year of the school year (ex: M1, L2, B3...)
    - :class:`str` label
    """
    structure_campus = models.OneToOneField(
        StructureCampus,
        verbose_name='Promotion',
        related_name='promotion_school_year',
        on_delete=models.PROTECT
    )
    contract_request = models.ForeignKey(
        ContractRequest,
        verbose_name='Promotion',
        related_name='contract_school_year',
        on_delete=models.PROTECT
    )
    year = models.CharField('Année', max_length=15, help_text='ex: M1')
    label = models.CharField('Nom', max_length=255)

    class Meta:
        verbose_name = 'Promotion'
        verbose_name_plural = 'Promotions'

    def __str__(self):
        return f'{self.year} - {self.label}'
