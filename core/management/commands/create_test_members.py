from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Member
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée des membres de test avec différents statuts'

    def handle(self, *args, **kwargs):
        # Membre actif
        user1, _ = User.objects.get_or_create(
            email='active@example.com',
            defaults={'first_name': 'John', 'last_name': 'Doe'}
        )
        member1, _ = Member.objects.get_or_create(
            user=user1,
            defaults={
                'member_type': 'active',
                'status': 'active',
                'membership_expiry': now().date() + timedelta(days=30),
                'monthly_fee': 50.00
            }
        )

        # Membre fondateur
        user2, _ = User.objects.get_or_create(
            email='founder@example.com',
            defaults={'first_name': 'Jane', 'last_name': 'Smith'}
        )
        member2, _ = Member.objects.get_or_create(
            user=user2,
            defaults={
                'member_type': 'founder',
                'status': 'active'
            }
        )

        self.stdout.write(self.style.SUCCESS('Membres de test créés avec succès'))