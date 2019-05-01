from rest_framework import serializers
from .models import blaster
import os
import magic

def check_query_input(query_file):
    """Checks file extension and mimetype"""
    allowed_mimes = ["text/plain",]
    allowed_extensions = [".fasta", ".ffn", ".fna"]
    extension = os.path.splitext(query_file.name)[1]
    if extension not in allowed_extensions:
        str_ext = ", ".join(allowed_extensions)
        raise serializers.ValidationError("allowed extensions {0}".format(str_ext), code="invalid")
    mime = magic.from_buffer(query_file.read(), mime=True)
    #check file_mime type
    if mime not in allowed_mimes:
        raise serializers.ValidationError(("Cachino, WTF??"), code="invalid")
    return query_file

def check_sequences_input(sequences_input_file):
    """Checks file extension and mimetype"""
    allowed_mimes = ["text/plain", "application/zip",
                     "application/x-tar", "application/x-gzip"]
    allowed_extensions = [".zip", ".tar", ".gz", ".fasta", ".ffn", ".fna"]
    extension = os.path.splitext(sequences_input_file.name)[1]
    if extension not in allowed_extensions:
        str_ext = ", ".join(allowed_extensions)
        raise serializers.ValidationError("allowed extensions {0}".format(str_ext), code="invalid")
    mime = magic.from_buffer(sequences_input_file.read(), mime=True)
    if mime not in allowed_mimes:
        raise serializers.ValidationError(("Cachino, WTF??"), code="invalid")
    return sequences_input_file

class BlasterIOSerializer(serializers.ModelSerializer):
    min_leng = serializers.FloatField(min_value=0, max_value=99999999999999999, label="Minimum hit length:", required=False)
    max_leng = serializers.FloatField(min_value=0, max_value=99999999999999999, label="Maximum hit length:", required=False)
    min_coverage = serializers.FloatField(min_value=0, max_value=100, label="Minimum hit coverage % value:", required=False)
    min_identity = serializers.FloatField(min_value=0, max_value=100, label="Minimum hit identity % value:", required=False)
    query_input = serializers.FileField(use_url=False)
    sequences_input = serializers.FileField(use_url=False)
    non_model_fields = ("min_leng", "max_leng", "min_coverage", "min_identity")
    def create(self, validated_data):
        """Excluding validated non model fields before creating model instance"""
        edited_validated_data = {key:value for (key, value) in validated_data.items() if key not in self.non_model_fields}
        return super().create(edited_validated_data)

    class Meta:
        model = blaster
        fields = ("id_num", "query_input", "sequences_input", "task", "sort_by", "sort_horizontal", "min_leng", "max_leng", "min_coverage", "min_identity")
        read_only_fields = ("id_num", )

    def validate_query_input(self, value):
        return check_query_input(value)

    def validate_sequences_input(self, value):
        return check_sequences_input(value)
