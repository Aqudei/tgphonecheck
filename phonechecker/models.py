from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
# Create your models here.


class PhoneNumber(models.Model):

    phone_number = models.CharField(_("Phone Number"), max_length=50)

    class Meta:
        verbose_name = _("phonenumber")
        verbose_name_plural = _("phonenumbers")

    def __str__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse("phonenumber_detail", kwargs={"pk": self.pk})
