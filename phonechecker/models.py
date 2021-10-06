from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from django.utils.translation import gettext as _
# Create your models here.


class PhoneNumber(models.Model):

    phone_number = models.CharField(_("Phone Number"), max_length=50)

    class Meta:
        verbose_name = _("phonenumber")
        verbose_name_plural = _("phonenumbers")

    def __str__(self):
        return "{}".format(self.phone_number)

    def get_absolute_url(self):
        return reverse("phonenumber_detail", kwargs={"pk": self.pk})


class Check(models.Model):
    RESULT_CHOICES = ((0, 'pending'), (1, 'has-tg'),
                      (2, 'no-username'), (3, 'error'))
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)
    phone_number = models.ForeignKey(PhoneNumber, verbose_name=_(
        "Phone Number"), on_delete=models.CASCADE)
    result = models.IntegerField(_("Result"), choices=RESULT_CHOICES)

    class Meta:
        verbose_name = _("check")
        verbose_name_plural = _("checks")

    def __str__(self):
        return "{} - {}".format(self.timestamp, self.phone_number)

    def get_absolute_url(self):
        return reverse("check_detail", kwargs={"pk": self.pk})
