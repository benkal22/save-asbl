from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from core.models import AboutSection, TeamMember, Partner, Achievement, Member

class Command(BaseCommand):
    help = 'Charge les données de test About dans la base de données'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Clean existing data
                User = get_user_model()
                
                # Delete related data first
                TeamMember.objects.all().delete()
                Partner.objects.all().delete()
                Achievement.objects.all().delete()
                AboutSection.objects.all().delete()
                
                # Delete test users (only those with @save-asbl.org emails)
                User.objects.filter(email__endswith='@save-asbl.org').delete()

                # Load fresh data
                from core.tests.test_about import AboutDataTestCase
                test_case = AboutDataTestCase()
                test_case.setUp()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Les données ont été chargées avec succès:')
                )
                self.stdout.write(
                    f'  • {AboutSection.objects.count()} sections About'
                )
                self.stdout.write(
                    f'  • {TeamMember.objects.count()} membres d\'équipe'
                )
                self.stdout.write(
                    f'  • {Partner.objects.count()} partenaires'
                )
                self.stdout.write(
                    f'  • {Achievement.objects.count()} réalisations'
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors du chargement des données: {str(e)}')
            )
            raise e