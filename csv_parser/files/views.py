import os
import mimetypes
from .models import Files
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, reverse
from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from csv_parser.files.db_functions import save, get_filename_by_id
from csv_parser.files.parser import (
    get_files_info,
    df_to_html,
    df_to_csv,
    get_column_names_and_rows,
    filter_data)


# Create your views here.
def upload_csv(request):
    """
    Uploading file and save it in model
    """
    if request.POST:
        try:
            csv_file = request.FILES["file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "File format is not CSV")
                return HttpResponseRedirect(reverse('upload'))
            if csv_file.multiple_chunks():
                messages.error(
                    request,
                    "Uploaded file is too big (%.2f MB). "
                    % (csv_file.size / (1000 * 1000),)
                )
                return HttpResponseRedirect(reverse('upload'))
            save(csv_file)
            messages.success(request, "File uploaded successfully")
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            messages.error(request, "Unable to upload file. " + repr(e))

    return render(request, 'files/upload.html')


class FilesIndexView(ListView):
    """
    List all files
    """
    model = Files
    template_name = 'files/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["files_info"] = get_files_info()
        return context


class FileDetailView(DetailView):
    """
    Show file data
    """
    model = Files

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["columns"], context["rows"] = get_column_names_and_rows(context["object"].file)
        return context


def show_data(request, pk):
    """Show all/filtered data from file"""
    if request.POST:
        columns_to_show = request.POST.getlist('select')
        columns_to_sort = request.POST.getlist('sort_values')
        is_desc = not bool(request.POST.get('is_desc'))
        is_index = bool(request.POST.get('is_index'))
        is_head = request.POST.get('is_head')
        number_of_rows = int(request.POST.get("rows_to_show"))
        filtered_data = filter_data(pk,
                                    columns_to_show,
                                    columns_to_sort,
                                    is_desc,
                                    is_index,
                                    is_head,
                                    number_of_rows)
        df_to_html(df=filtered_data, pk=pk)
        df_to_csv(filtered_data, pk)

    return render(request, 'files/frames.html')


def download_file(request, pk):
    """
    Download file from server
    """
    file_name = get_filename_by_id(pk)
    file_path = settings.BASE_DIR / settings.MEDIA_ROOT / 'downloadedfiles' / file_name
    with open(file_path, 'r') as f:
        mime_type = mimetypes.guess_type(file_path)
        response = HttpResponse(f, content_type=mime_type)
        response["Content-Disposition"] = "attachment; filename=%s" % file_name
    return response


class FileDeleteView(SuccessMessageMixin, DeleteView):
    """
    Delete file from db
    """
    model = Files
    template_name = 'files/delete.html'
    context_object_name = 'file'
    success_url = reverse_lazy('index')
    success_message = "File successfully deleted"

    def form_valid(self, form):
        success_url = self.get_success_url()
        download_file = settings.BASE_DIR / settings.MEDIA_ROOT / 'downloadedfiles' / self.object.file_name
        upload_file = settings.BASE_DIR / settings.MEDIA_ROOT / 'uploadedfiles' / self.object.file_name
        if os.path.exists(download_file):
            os.remove(download_file)
        os.remove(upload_file)
        self.object.delete()

        return HttpResponseRedirect(success_url)
