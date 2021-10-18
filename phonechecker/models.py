from logging import debug
from uuid import uuid4
from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

# Create your models here.


class PhoneNumber(models.Model):

    phone_number = CharField(_("Phone Number"), max_length=100)
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _("phonenumber")
        verbose_name_plural = _("phonenumbers")

    def __str__(self):
        return "{}".format(self.phone_number)

    def get_absolute_url(self):
        return reverse("phonenumber_detail", kwargs={"pk": self.pk})


class Check(models.Model):

    RESULT_CHOICES = ((0, 'pending'), (1, 'has-tg'),
                      (2, 'no-username'), (3, 'error'), (4, 'processing'))
    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)
    phone_number = models.ForeignKey(PhoneNumber, verbose_name=_(
        "Phone Number"), on_delete=models.CASCADE)
    result = models.IntegerField(
        _("Result"), choices=RESULT_CHOICES, default=0)
    batch = models.CharField(_("Batch"), max_length=80, default='dummy-uuid')
    debug = models.TextField(_("Debug"), blank=True, null=True)
    username = models.CharField(
        _("Username"), max_length=250, null=True, blank=True)
    source = models.CharField(
        _("Source"), max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = _("check")
        verbose_name_plural = _("checks")

    def __str__(self):
        return "{} - {}".format(self.timestamp, self.phone_number)

    def get_absolute_url(self):
        return reverse("check_detail", kwargs={"pk": self.pk})


class Upload(models.Model):

    file = models.FileField(_("Upload"), upload_to=None, max_length=100)
    phone_column = models.CharField(
        _("Column Name"), max_length=200, default='PhoneNumbers')
    batch_id = models.CharField(
        _("Batch Id"), max_length=100, null=True, blank=True, default=uuid4)
    remarks = models.TextField(_("Remarks"), null=True, blank=True, default='')

    class Meta:
        verbose_name = _("upload")
        verbose_name_plural = _("uploads")

    def __str__(self):
        return "{}-{}".format(self.phone_column, self.file)

    def get_absolute_url(self):
        return reverse("upload_detail", kwargs={"pk": self.pk})


class BotLogin(models.Model):
    batch = models.CharField(_("Batch"), max_length=100)
    done = models.BooleanField(_("Done"), default=False)
    phone_number = CharField(_("Phone Number"), max_length=100)
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


class MySql(models.Model):
    batch_id = models.CharField(
        _("Batch Id"), max_length=100, null=True, blank=True, default=uuid4)
    db_name = models.CharField(_("DB Name"), max_length=100)
    db_username = models.CharField(_("DB Username"), max_length=100)
    db_password = models.CharField(_("DB Password"), max_length=100)
    db_host = models.CharField(_("DB Host"), max_length=100)
    db_port = models.IntegerField(_("DB Port"), default=3306)
    db_table = models.CharField(_("DB Table Name"), max_length=100)
    db_column = models.CharField(_("DB Column Name"), max_length=100)

    timestamp = models.DateTimeField(
        _("Timestamp"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("mysql")
        verbose_name_plural = _("mysqls")

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}-{}".format(
            self.db_name, self.db_username, self.db_host, self.db_port, self.db_table, self.db_column, self.timestamp)

    def get_absolute_url(self):
        return reverse("mysql_detail", kwargs={"pk": self.pk})
