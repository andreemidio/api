import pytz
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import AbstractAPIKey
from rest_framework.views import APIView
import base64


# Create your models here.


class EmailUserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        email = kwargs["email"]
        email = self.normalize_email(email)
        password = kwargs["password"]
        kwargs.pop("password")

        if not email:
            raise ValueError(_('Necessário um email válido'))

        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(PermissionsMixin, AbstractBaseUser,APIView):
    nome = models.CharField(
        verbose_name=_('Nome'), max_length=255, blank=False, help_text=_('Informe seu nome')
    )
    sobrenome = models.CharField(
        verbose_name=_('Sobrenome'), max_length=255, blank=False, help_text=_('Informe seu sobrenome')
    )
    email = models.EmailField(
        verbose_name=_('Email'), unique=True, max_length=255
    )
    reset_pass = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    objects = EmailUserManager()

    #permission_classes = [HasAPIKey]

    def __str__(self):
        return "{} | {}".format(self.id, self.email)

    def __repr__(self):
        return "{} | {}".format(self.id, self.email)

    @property
    def ativo_human(self):
        return 'Sim' if self.is_active else 'Não'

    class Meta:
        verbose_name = 'UsuariosAcesso'



class UserAPIKey(AbstractAPIKey):
    organization = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    class Meta(AbstractAPIKey.Meta):
        verbose_name = "Usuario API key"
        verbose_name_plural = "Usuarios API keys"

class Documentos(models.Model):
    cpf_ou_cnpj = models.CharField(max_length=255, null=False, blank=True)
    celular = models.CharField(max_length=255, null=False, blank=True)
    resultado_consultas = models.TextField(null=False, blank=True)
    documento_identificacao = models.BinaryField(null=False, blank=True)
    selfie_usuario = models.BinaryField(null=False, blank=True)
    comprovante_residencia = models.BinaryField(null=False, blank=True)

    class Meta:
        verbose_name = 'DocumentosConsulta'

    def __str__(self):
        return self.cpf_ou_cnpj, \
               self.nome, \
               self.celular, \
               self.resultado_consultas, \
               self.documento_identificacao, \
               self.selfie_usuario, \
               self.comprovante_residencia


class Consultas(models.Model):
    data = models.DateTimeField(null=False, blank=True)
    usuarioID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    documentoID = models.ForeignKey(Documentos, on_delete=models.CASCADE)

    class Meta:
        verbose_name =  'Consultas'


class LogConsulta(models.Model):
    data_consulta = models.DateTimeField(null=False, blank=True)
    valor = models.TextField(null=False, blank=True)
    usuarioID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    documentoID = models.ForeignKey(Documentos, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'LogConsulta'

    def __str__(self):
        return self.data_consulta, \
               self.valor, \
               self.usuarioID, \
               self.documentoID
