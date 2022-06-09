from django.db import models


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
    pass


class StructureCampus(models.Model):
    """
    Value of structure or campus

    Attributes:

    - :class:`ContractRequest` contract_request
    - :class:`string` label -> Name of the campus or structure
    """
    contract_request = models.ForeignKey(ContractRequest, verbose_name='Nom ou structure', on_delete=models.PROTECT)
    label = models.CharField(verbose_name='Nom', max_length=20)
