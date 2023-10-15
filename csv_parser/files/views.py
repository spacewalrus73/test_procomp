from .models import Files
from django.contrib import messages
from django.views.generic import View
from django.views.generic import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.list import ListView
from django.shortcuts import render, reverse, get_object_or_404
from csv_parser.files.parser import (
    get_files_info,
    save,
    df_to_html,
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
        context["files"] = get_files_info()
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
        is_ascending = bool(request.POST.get('is_ascending'))
        is_index = bool(request.POST.get('is_index'))
        is_head = request.POST.get('is_head')
        number_of_rows = int(request.POST.get("rows_to_show"))
        filtered_data = filter_data(pk,
                                    columns_to_show,
                                    columns_to_sort,
                                    is_ascending,
                                    is_index,
                                    is_head,
                                    number_of_rows)
        frame = df_to_html(df=filtered_data)
        with open('csv_parser/templates/files/frames.html', 'w') as f:
            f.write(frame)

    return render(request, 'files/frames.html')
