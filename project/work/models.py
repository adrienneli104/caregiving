from django.core.validators import MinValueValidator
from django.db.models import CheckConstraint, Q
from django.db import models
from django.utils.translation import gettext_lazy as _

from caregivers.models import CaregiverRole
from homes.models import Home

minutes_in_hour = 60


class WorkType(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        db_table = "work_type"
        verbose_name = _("work type")
        verbose_name_plural = _("work types")

    def __str__(self) -> str:
        return self.name


class Work(models.Model):
    home = models.ForeignKey(Home, related_name="work_performed", on_delete=models.CASCADE, help_text=_("The home in which this work was performed."))
    type = models.ForeignKey(WorkType, related_name="+", on_delete=models.PROTECT, help_text=_("The general type of work performed."))
    caregiver_role = models.ForeignKey(CaregiverRole, related_name="+", on_delete=models.PROTECT, help_text=_("The role or job title of the person who performed this work."))
    date = models.DateField(help_text=_("The date this work was performed."))
    duration = models.PositiveIntegerField(help_text=_("The number of minutes used performing this work."))
    duration_hours = models.FloatField(
        validators=[MinValueValidator(0.0),]
    )

    class Meta:
        db_table = "work"
        verbose_name = _("work")
        verbose_name_plural = _("work")
        constraints = (
            CheckConstraint(
                check=Q(duration_hours__gte=0.0),
                name='work_duration_hours_gte_zero'
            ),
        )
    
    def save(self, *args, **kwargs):
        self.duration_hours = self.duration / minutes_in_hour
        super(Work, self).save(*args, **kwargs)

    def __str__(self):
        return f"{ self.home } - { self.caregiver_role } - { self.type } - { self.date } - { self.duration }"
