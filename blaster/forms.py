from django import forms
from .models import blaster
from django.core.validators import FileExtensionValidator
import magic
import os



class blaster_form(forms.ModelForm):
    """ModelForm for user sequences and analysis parameters input

    Attributes:
        min_leng, max_leng, min_coverage, min_identity: FormFields for analysis parameters
    """

    min_leng = forms.FloatField(min_value=0, max_value=99999999999999999, label="Minimum hit length:", required=False)
    max_leng = forms.FloatField(min_value=0, max_value=99999999999999999, label="Maximum hit length:", required=False)
    min_coverage = forms.FloatField(min_value=0, max_value=100, label="Minimum hit coverage % value:", required=False)
    min_identity = forms.FloatField(min_value=0, max_value=100, label="Minimum hit identity % value:", required=False)
    class Meta:
        model = blaster # model object
        fields = ["task", "sort_by", "sort_horizontal", "query_input", "sequences_input",] # list of model fields objects
        labels = {
        "task": "Task:", "sort_by": "Sort hits by:", "sort_horizontal": "Sort horizontally:",
        } # custom form fields labels

    def clean_sequences_input(self):
        """blaster_form clean method, validates user subject file input extension and mimetype

        Raise:
            ValidationError: if user subject file input is not appropriate
        Returns:
            cleaned user input files"""

        allowed_mimes = ["text/plain", "application/zip",
                         "application/x-tar", "application/x-gzip"]
        allowed_extensions = [".zip", ".tar", ".gz", ".fasta", ".ffn", ".fna"]
        sequences_input_file = self.cleaned_data["sequences_input"]
        extension = os.path.splitext(sequences_input_file.name)[1]
        if extension not in allowed_extensions:
            str_ext = ", ".join(allowed_extensions)
            raise forms.ValidationError("allowed extensions {0}".format(str_ext), code="invalid")
        mime = magic.from_buffer(sequences_input_file.read(), mime=True)
        if mime not in allowed_mimes:
            raise forms.ValidationError(("WTF??"), code="invalid")
        return sequences_input_file


    def clean_query_input(self):
        """blaster_form clean method, validates user query file input extension and mimetype

        Raise:
            ValidationError: if user query file input is not appropriate
        Returns:
            cleaned user input files"""
        allowed_mimes = ["text/plain",]
        allowed_extensions = [".fasta", ".ffn", ".fna"]
        query_file = self.cleaned_data["query_input"]
        extension = os.path.splitext(query_file.name)[1]
        if extension not in allowed_extensions:
            str_ext = ", ".join(allowed_extensions)
            raise forms.ValidationError("allowed extensions {0}".format(str_ext), code="invalid")
        mime = magic.from_buffer(query_file.read(), mime=True)
        #check file_mime type
        if mime not in allowed_mimes:
            raise forms.ValidationError(("WTF??"), code="invalid")
        return query_file
