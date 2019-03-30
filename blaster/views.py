from django.shortcuts import render
from django.views.generic import CreateView
from .forms import blaster_form
from .models import blaster# Create your views here.
import uuid
from django.urls import reverse, reverse_lazy
from .tool.make_excel_for_cds_for_public import blaster_tool
from .tool.remove_cache import remove_cache
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import io

# removes blaster tool database records and delete users uploaded files and folders
# def clear_blaster_tool_cache_and_database():
#     remove_cache()
#     for i in blaster.objects.all():
#         print(i)
#         i.delete()



class Blaster(CreateView):
    form_class = blaster_form
    template_name = "blaster.html"
    #queryset = blaster.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["id_num"] = self.kwargs["output_id"]
        except:
            pass
        return context

    def form_valid(self, form):
        self.object = form.save()

        id_num_corrected = str(self.object.id_num).replace("-", "")
        id_path = "{0}\\{1}".format(settings.TEST_ROOT, id_num_corrected)
        query_name = self.request.FILES["query_input"]
        sort_by = form.cleaned_data["sort_by"]
        sort_horizontal = form.cleaned_data["sort_horizontal"]

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
        #print(form.cleaned_data)

        run_blaster = blaster_tool(id_num=id_path, query_name=query_name, task=self.object.task,
                                   sort_by=sort_by, sort_horizontal=sort_horizontal,
                                   min_leng=min_leng, max_leng=max_leng,
                                   min_coverage=min_coverage, min_identity=min_identity)
        run_blaster.create_id_folder()
        run_blaster.unpack_sequences()
        run_blaster.db_blast()
        run_blaster.make_excel()
        output_id = id_num_corrected
        return redirect("blaster", output_id)


def download_file(request, output_id):
    return FileResponse(open("{0}\\{1}\\output.xlsx".format(settings.TEST_ROOT, output_id), "rb"), as_attachment=True, filename="out.xlsx")
#
