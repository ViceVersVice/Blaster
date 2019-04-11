from rest_framework import serializers
from .models import blaster


class BlasterIOSerializer(serializers.ModelSerializer):
    min_leng = serializers.FloatField(min_value=0, max_value=99999999999999999, label="Minimum hit length:", required=False)
    max_leng = serializers.FloatField(min_value=0, max_value=99999999999999999, label="Maximum hit length:", required=False)
    min_coverage = serializers.FloatField(min_value=0, max_value=100, label="Minimum hit coverage % value:", required=False)
    min_identity = serializers.FloatField(min_value=0, max_value=100, label="Minimum hit identity % value:", required=False)
    non_model_fields = ("min_leng", "max_leng", "min_coverage", "min_identity")
    def create(self, validated_data):
        """Excluding validated non model fields before creating model instance"""
        validated_data = {key:value for (key, value) in validated_data.items() if key not in self.non_model_fields}
        return super().create(validated_data)

    class Meta:
        model = blaster
        fields = ("id_num", "query_input", "sequences_input", "task", "sort_by", "sort_horizontal", "min_leng", "max_leng", "min_coverage", "min_identity",)
        read_only_fields = ("id_num", )
