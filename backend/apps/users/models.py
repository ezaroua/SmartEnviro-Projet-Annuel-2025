from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class Role(models.Model):
    """Rôle utilisateur (admin ou citoyen)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du rôle")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    
    class Meta:
        db_table = 'role'
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        
    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    """Gestionnaire pour le modèle utilisateur personnalisé"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        """Créer et enregistrer un utilisateur"""
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        """Créer et enregistrer un super-utilisateur"""
        # Récupérer ou créer le rôle admin
        role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Administrateur avec accès complet'}
        )
        
        extra_fields.setdefault('role', role)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé compatible avec la table MySQL existante"""
    username = models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur")
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Prénom")
    last_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nom")
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, db_column='role_id', verbose_name="Rôle")
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Téléphone")
    address = models.TextField(null=True, blank=True, verbose_name="Adresse")
    receive_alerts = models.BooleanField(default=True, verbose_name="Recevoir des alertes")
    preferred_district = models.CharField(max_length=100, null=True, blank=True, verbose_name="Quartier préféré")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date d'inscription")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Dernière connexion")
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'users'
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
  
    def save(self, *args, **kwargs):

        if self.role and self.role.name == 'admin':
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        
        super().save(*args, **kwargs)
    
    def is_admin(self):
        """Vérifier si l'utilisateur est administrateur"""
        return self.role.name == 'admin'
        
    def is_citizen(self):
        """Vérifier si l'utilisateur est citoyen"""
        return self.role.name == 'citizen'
        
    def get_full_name(self):
        """Obtenir le nom complet de l'utilisateur"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username