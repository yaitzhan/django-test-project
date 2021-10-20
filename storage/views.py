import os
import logging

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponseNotFound, HttpResponse

from .forms import FileUploadForm
from .models import FileUpload, FileUploadSequence
from .helpers import combine_result_file_from_zips


logger = logging.getLogger('app-logger')


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = FileUpload.objects.all()
        return context


class FileUploadView(CreateView):
    model = FileUpload
    form_class = FileUploadForm
    success_url = reverse_lazy('home')
    template_name = 'file_upload.html'

    def post(self, request, *args, **kwargs):
        logger.info('New file uploaded')
        return super().post(request, *args, **kwargs)


class FileDownloadView(View):
    def get(self, request, file_id):
        file_obj = FileUpload.objects.get(id=file_id)
        file_sequence_obj = FileUploadSequence.objects.get(file_upload__pk=file_id)

        combine_result_file_from_zips(file_sequence_obj.sequence, file_obj.upload.name)

        file_path = file_obj.upload.path
        file_content_type = file_obj.upload.path

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
                response = HttpResponse(content, content_type=file_content_type)
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            try:
                logger.info('The file downloaded')
                return response
            finally:
                os.remove(file_path)
        else:
            raise HttpResponseNotFound
