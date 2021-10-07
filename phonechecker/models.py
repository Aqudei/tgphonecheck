from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class PhoneNumber(models.Model):

    phone_number = PhoneNumberField(_("Phone Number"))

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
    result = models.IntegerField(
        _("Result"), choices=RESULT_CHOICES, default=0)
    batch = models.CharField(_("Batch"), max_length=80, default='dummy-uuid')

    class Meta:
        verbose_name = _("check")
        verbose_name_plural = _("checks")

    def __str__(self):
        return "{} - {}".format(self.timestamp, self.phone_number)

    def get_absolute_url(self):
        return reverse("check_detail", kwargs={"pk": self.pk})


class BotLogin(models.Model):
    batch = models.CharField(_("Batch"), max_length=100)
    done = models.BooleanField(_("Done"), default=False)
    phone_number = PhoneNumberField(_("Phone Number"))
    code = models.CharField(_("Code"), max_length=50,
                            default='', null=True, blank=True)
    two_factor = models.CharField(
        _("Two Factor"), max_length=50, default='', null=True, blank=True)
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("botlogin")
        verbose_name_plural = _("botlogins")

    def __str__(self):
        return "{}".format(self.phone_number)

    def get_absolute_url(self):
        return reverse("botlogin_detail", kwargs={"pk": self.pk})
