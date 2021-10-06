from rest_framework import serializers
from phonechecker.models import *


class CheckSerializer(serializers.ModelSerializer):
    """
    docstring
    """
    class Meta:
        model = Check
        fields = "__all__"
