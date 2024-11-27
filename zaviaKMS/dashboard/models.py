from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Para usar el modelo UserApp

class UserApp(AbstractUser):
    """
    Modelo independiente para usuarios en la app, sin conflictos con el modelo User de Django.
    """
    
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('pm', 'Project Manager'),
        ('developer', 'Developer'),
    )

    # Campo adicional para el rol
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='developer',  # Asigna un valor predeterminado
    )
    email = models.EmailField(max_length=254, blank=True, verbose_name='email address')
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        verbose_name='active',
    )
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')  # Corregido: no uses "now"

    class Meta:
        verbose_name = 'user app'
        verbose_name_plural = 'users app'

    def __str__(self):
        return self.username


class Report(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('mid', 'Mid'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('update', 'Update'),
    ]

    STATUS_CHOICES = [
        ('WIP', 'Work in Progress'),
        ('DONE', 'Done'),
        ('CLOSED', 'Closed'),
    ]    
    title = models.CharField(max_length=150, verbose_name='Title')  # Nuevo campo para el título
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_reports',
        verbose_name='Created By',
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports',
        verbose_name='Assigned To',
    )
    affected_product = models.CharField(max_length=150, verbose_name='Affected Product')
    description = models.TextField(verbose_name='Description')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, verbose_name='Priority')
    tags = models.JSONField(default=list, verbose_name='Tags')  # Para almacenar múltiples etiquetas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WIP')  # Valor por defecto
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modified At')

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username} - {self.affected_product}"  # Ahora incluye el título
