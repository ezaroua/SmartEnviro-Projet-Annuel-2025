from django.core.management.base import BaseCommand
from apps.users.models import Role


class Command(BaseCommand):
    help = 'Initialize database with default roles'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database with default roles...')
        
        # Create default roles
        admin_role, admin_created = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Administrateur avec accès complet'}
        )
        
        citizen_role, citizen_created = Role.objects.get_or_create(
            name='citizen',
            defaults={'description': 'Citoyen avec accès limité'}
        )
        
        if admin_created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created admin role: {admin_role.name}')
            )
        else:
            self.stdout.write(f'✓ Admin role already exists: {admin_role.name}')
        
        if citizen_created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created citizen role: {citizen_role.name}')
            )
        else:
            self.stdout.write(f'✓ Citizen role already exists: {citizen_role.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Database initialization completed successfully!')
        )