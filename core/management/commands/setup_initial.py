from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from core.models import create_user_groups
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Configure l\'installation initiale de l\'application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Démarrage de la configuration initiale...'))
        
        # Migrations
        self.stdout.write('⚙️ Application des migrations...')
        call_command('makemigrations')
        call_command('migrate')

        # Create groups
        self.stdout.write('👥 Création des groupes...')
        create_user_groups()

        # Create superuser if not exists
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('👤 Création du super utilisateur...')
            User.objects.create_superuser(
                email='benkalsoft@gmail.com',
                password='diansosa2020',
                role='superadmin'
            )

        self.stdout.write(self.style.SUCCESS('✅ Configuration initiale terminée!'))