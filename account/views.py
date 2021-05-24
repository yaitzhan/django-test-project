from .models import CustomUser

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users.html'

    def get(self, request):
        queryset = CustomUser.objects.all()
        return Response({'users': queryset})
