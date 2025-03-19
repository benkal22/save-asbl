from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Configure l\'environnement de développement'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Démarrage de la configuration...'))
        
        # Création des dossiers nécessaires
        folders = ['static', 'static/src', 'media', 'staticfiles']
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                self.stdout.write(self.style.SUCCESS(f'✅ Dossier {folder} créé'))

        # Migrations
        self.stdout.write(self.style.SUCCESS('\n🔄 Application des migrations...'))
        call_command('makemigrations')
        call_command('migrate')

        # Collectstatic
        self.stdout.write(self.style.SUCCESS('\n📦 Collecte des fichiers statiques...'))
        call_command('collectstatic', '--noinput')

        # Installation des dépendances npm
        self.stdout.write(self.style.SUCCESS('\n📦 Installation des dépendances npm...'))
        os.system('npm install')

        # Compilation Tailwind
        self.stdout.write(self.style.SUCCESS('\n🎨 Compilation de Tailwind CSS...'))
        os.system('npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css')

        self.stdout.write(self.style.SUCCESS('\n✨ Configuration terminée avec succès!'))