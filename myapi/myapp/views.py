from rest_framework import generics
from .models import Documentos
from .serializers import DocumentosSerializer

# Create your views here.


class DocumentList(generics.ListCreateAPIView):

    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer