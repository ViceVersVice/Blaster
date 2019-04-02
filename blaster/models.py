from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

blaster_storage = FileSystemStorage(location=settings.TEST_ROOT, base_url='/Project/tool/')
"""Define custom file storage for uploaded user sequences input"""
# query_validator = FileExtensionValidator(allowed_extensions=["fasta", "ffn", "fna"])
# sequences_validator = FileExtensionValidator(allowed_extensions=["fasta", "ffn", "fna", "zip", "gz", "tar"])



def upload_query(instance, filename):
    """Generates unique folder path for user query sequences input"""

    id_num_corrected = str(instance.id_num).replace("-", "")
    return "{0}/{1}".format(id_num_corrected, filename)

def upload_sequences(instance, filename):
    """Generates unique folder path for user subject sequences input"""

    id_num_corrected = str(instance.id_num).replace("-", "")
    return "{0}/sequences/{1}".format(id_num_corrected, filename)


class blaster(models.Model):
    """Database Model for user input sequence files and analysis parameters.
       Provides for each user analysis request unique uuid.

    Attributes:
        BLASTN, MEGABLAST, SCORE, E_VALUE, COVERAGE, IDENTITY, QUERY_START,
        SUBJECT_START, NO_SORTING: analysis parameters
        ..._choices: choices with analysis parameters
        sort_by, sort_horizontal, task : model fields for analysis parameteres
        id_num: UUIDField, model field. Defines uuid, which is saved with validated user input
        query_input: FileField, model field. Defines path to query sequence input
        sequences_input: FileField, model field. Defines path to subject sequences input
    """

    BLASTN, MEGABLAST = "blastn", "megablast"
    SCORE, E_VALUE, COVERAGE, IDENTITY = "score", "e_value", "coverage", "identity"
    QUERY_START, SUBJECT_START, NO_SORTING =  "query_start", "subject_start", "without sorting"

    task_choices = [(BLASTN, "blastn"), (MEGABLAST, "megablast"), ]
    sort_by_choices = [(SCORE, "Score"), (E_VALUE, "e_value"), (COVERAGE, "Coverage"),
    (IDENTITY, "Identity"), (QUERY_START, "Query_start"), (SUBJECT_START, "Subject_start"), ]
    sort_horizontal_choices = [(NO_SORTING, "Without sorting"), (SCORE, "Score"), (E_VALUE, "e_value"), (COVERAGE, "Coverage"), ]
    sort_by = models.CharField(max_length=20, choices=sort_by_choices, default=SCORE)
    sort_horizontal = models.CharField(max_length=20, choices=sort_horizontal_choices, default=NO_SORTING)
    task = models.CharField(max_length=10, choices=task_choices, default=MEGABLAST)
    id_num = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query_input = models.FileField(upload_to=upload_query, storage=blaster_storage)
    sequences_input = models.FileField(upload_to=upload_sequences, storage=blaster_storage)
    def __str__(self):
        return str(self.id_num)
