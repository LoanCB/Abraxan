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
    comment = models.CharField('Commentaire', max_length=256, null=True, blank=True)
    status = models.PositiveSmallIntegerField('Statut', choices=STATUS, max_length=4, default=WAITING_DOC)
    applied_rate = models.FloatField('Tarif à appliquer')
    ttc = models.BooleanField('Toute Taxes Comprises', help_text='SST si faux', default=True)
    hourly_volume = models.FloatField('Volume horaire')


class StructureCampus(models.Model):
    """
    Value of structure or campus

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label -> Name of the campus or structure
    """
    contract_request = models.ForeignKey(ContractRequest, verbose_name='Nom ou structure', on_delete=models.PROTECT)
    label = models.CharField('Nom', max_length=20)


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
    contract_request = models.ForeignKey(ContractRequest, verbose_name='Intervenant', on_delete=models.PROTECT)
    first_name = models.CharField('Prénom', max_length=50)
    last_name = models.CharField('Nom', max_length=100)
    civility = models.CharField('Civilité', max_length=1, choices=CIVILITY, default=MEN)
    company_type = models.CharField('Type de la société', max_length=255, blank=True, null=True)
    mail = models.EmailField()
    phone_number = PhoneNumberField(verbose_name='Numéro de téléphone', null=True, blank=True)


class Performance(models.Model):
    """
    A performance reattached to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label
    """
    contract_request = models.ForeignKey(ContractRequest, verbose_name='Prestation', on_delete=models.PROTECT)
    label = models.CharField('Nom', max_length=255)


class RateType(models.Model):
    """
    A rate type reattached to a contract request

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`str` label
    """
    contract_request = models.ForeignKey(ContractRequest, verbose_name='Type de tarif', on_delete=models.PROTECT)
    label = models.CharField('Nom', max_length=255)
