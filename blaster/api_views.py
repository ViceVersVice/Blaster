from rest_framework.generics import CreateAPIView, ListCreateAPIView
from .serializers import BlasterIOSerializer
from .models import blaster
from django.urls import reverse, reverse_lazy
from django.conf import settings
from .tool.make_excel_for_cds_for_public import blaster_tool
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import re

class BlasterIOApiView(CreateAPIView):
    serializer_class = BlasterIOSerializer
    #queryset = blaster.objects.all()
    #parser_classes = (FileUploadParser,)
    #permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        complemented_data = serializer.data
        for key in serializer.validated_data.keys():
            """Adds validated non model fields data to response (like in Django model forms)"""
            if key not in complemented_data.keys():
                complemented_data[key] = serializer.validated_data[key]
        non_parameters = ("id_num", "query_input", "sequences_input") # not needed to init blaster_tool()
        parameters = {key:value for (key, value) in complemented_data.items() if key not in non_parameters} # blaster_tool() init parameters
        query_name = re.split("/", complemented_data["query_input"])[-1] # query file name
        id_num_corrected = str(complemented_data["id_num"]).replace("-", "") # replaced dashes in uid
        id_path = "{0}\\{1}".format(settings.TEST_ROOT, id_num_corrected) # unique path to user input folder
        """Runs script with initialized parameters"""
        run_blaster = blaster_tool(id_num=id_path, query_name=query_name, **parameters)
        run_blaster.create_id_folder() # creates subfolders
        run_blaster.unpack_sequences() # unpack archivised files
        run_blaster.db_blast() # creates local BLAST sequence database and makes main analysis
        run_blaster.make_excel() # makes excel with results
        OUTPUT_URL = reverse_lazy("download_file", kwargs={"output_id": id_num_corrected, })
        complemented_data["OUTPUT_URL"] = OUTPUT_URL
        return Response(complemented_data, status=status.HTTP_201_CREATED, headers=headers)

    # def dispatch(self, request, *args, **kwargs):
    #     request1 = self.initialize_request(self.request, *args, **kwargs)
    #     #print("ALL:", vars(request1))
    #     print("Session:", request1.session)
    #     #print("META:", request1.META)
    #     print("USER:", request1.user.is_authenticated)
    #     print("AUTH:", request1.auth)
    #     #print("AUTH:", request1.authenticators)
    #     return super().dispatch(request, *args, **kwargs)
    # def initial(self, request, *args, **kwargs):
    #     print(request.user)
