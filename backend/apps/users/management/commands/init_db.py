from django.core.management.base import BaseCommand
from django.db import connection
from apps.users.models import Role

class Command(BaseCommand):
    help = 'Initialize database with roles and handle table conflicts'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database...')
        
        # Create roles if they don't exist
        admin_role, created = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Administrateur avec accès complet au système'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created admin role'))
        else:
            self.stdout.write('Admin role already exists')
            
        citizen_role, created = Role.objects.get_or_create(
            name='citizen',
            defaults={'description': 'Citoyen avec accès limité aux fonctionnalités de consultation'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created citizen role'))
        else:
            self.stdout.write('Citizen role already exists')
            
        self.stdout.write(self.style.SUCCESS('Database initialization completed')) 