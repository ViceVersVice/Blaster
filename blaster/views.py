from django.shortcuts import render
from django.views.generic import CreateView
from .forms import blaster_form
from .models import blaster# Create your views here.
import uuid
import os
from django.urls import reverse, reverse_lazy
from .tool.make_excel_for_cds_for_public import blaster_tool
from .tool.remove_cache import remove_cache
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import io


BLASTER_OUTPUT_PATH = os.path.join(settings.BASE_DIR, "blaster\\tool")
#print(BLASTER_OUTPUT_PATH)
#
# files and folders
def clear_blaster_tool_cache_and_database(root):
    """Removes blaster_tool database records and delete users uploaded data

    Args:
        root: path to folder with user input subfolders"""

    remove_cache(root)
    for i in blaster.objects.all():
        print(i)
        i.delete()

#clear_blaster_tool_cache_and_database(BLASTER_OUTPUT_PATH)


class Blaster(CreateView):
    """Represents user nucleotide sequences input and .xlsx result output

    This CBV represents user input and analysis parameters form, creates
    database record (see CreateView), validates these parameters, instantiates Blaster script class
    and calls it`s methods and provides link to file output.

    Overwritten attributes
    ----------
    form_class: object
        form class object
    template_name: str
        html template name
    """

    form_class = blaster_form
    template_name = "blaster.html"
    #queryset = blaster.objects.all()
    def get_context_data(self, **kwargs):
        """After submitting form provides output file link based on unique id

        kwargs:
            output_id: uuid of accepted by user form
        Returns:
            Context to html template. Also returns link to output file if provided output_id
        """

        context = super().get_context_data(**kwargs)
        try:
            context["id_num"] = self.kwargs["output_id"]
        except:
            pass
        return context

    def form_valid(self, form):
        """After successful form validation creates database record, creates
        instance of blaster_tool class and calls it`s methods

        args:
            form: validated form
        Returns:
            Redirect to Blaster view with output file uuid (output_id)
        """

        self.object = form.save()
        id_num_corrected = str(self.object.id_num).replace("-", "") #replaces unnecessary "-" in uuid
        output_id = id_num_corrected # output file id
        id_path = "{0}\\{1}".format(settings.TEST_ROOT, id_num_corrected) # path to user input files folder

        query_name = self.request.FILES["query_input"] # user quey file name
        sort_by = form.cleaned_data["sort_by"] # sorting parameter
        sort_horizontal = form.cleaned_data["sort_horizontal"] # sorting parameter
        # creates necessary initial parameters if they were not provided
        if form.cleaned_data["min_leng"] != None:
            min_leng = form.cleaned_data["min_leng"]
        else:
            min_leng=0
        if form.cleaned_data["max_leng"] != None:
            max_leng = form.cleaned_data["max_leng"]
        else:
            max_leng=9999999999999999999
        if form.cleaned_data["min_coverage"] != None:
            min_coverage = form.cleaned_data["min_coverage"]
        else:
            min_coverage=0
        if form.cleaned_data["min_identity"] != None:
            min_identity = form.cleaned_data["min_identity"]
        else:
            min_identity=0
        # creates instance of blaster_tool class with user input data and path to sequence files
        run_blaster = blaster_tool(id_num=id_path, query_name=query_name, task=self.object.task,
                                   sort_by=sort_by, sort_horizontal=sort_horizontal,
                                   min_leng=min_leng, max_leng=max_leng,
                                   min_coverage=min_coverage, min_identity=min_identity)
        run_blaster.create_id_folder() # creates subfolders
        run_blaster.unpack_sequences() # unpack archivised files
        run_blaster.db_blast() # creates local BLAST sequence database and makes main analysis
        run_blaster.make_excel() # creates .xlsx file wit output data
        return redirect("blaster", output_id) # refreshes page after analysis end


def download_file(request, output_id):
    """Provides .xlsx output with processed user data"""
    return FileResponse(open("{0}\\{1}\\output.xlsx".format(settings.TEST_ROOT, output_id), "rb"), as_attachment=True, filename="out.xlsx")
#
