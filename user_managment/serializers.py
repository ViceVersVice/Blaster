from rest_framework import serializers
from .models import blaster


class BlasterIOSerializer(serializers.ModelSerializer):

    class Meta:
        model = blaster
        fields = ("id_num", "query_input", "sequences_input", "task", "sort_by", "sort_horizontal")
        read_only_fields = ("id_num",)
