from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^nova-consulta/$',views.DocumentList.as_view(), name='nova-consulta'),
    url(r'log-consulta/$', views.LogConsultaList.as_view(), name='log-consulta')
]