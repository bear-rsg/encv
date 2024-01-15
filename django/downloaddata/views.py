from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from . import excel
import os


@login_required
def download_data_excel(request):
    """
    Creates an Excel workbook/spreadsheet and return it to the user
    """

    file_path = excel.create_workbook(request)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
            return response
    raise Http404
