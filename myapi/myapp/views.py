from rest_framework import generics
from .models import Documentos, LogConsulta
from .serializers import DocumentosSerializer, LogConsultaSerializer

# Create your views here.
class LogConsultaList(generics.ListAPIView):
    queryset = LogConsulta.objects.all()
    serializer_class = LogConsultaSerializer

class DocumentList(generics.ListCreateAPIView):

    queryset = Documentos.objects.all()
    serializer_class = DocumentosSerializer
