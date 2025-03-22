from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import AboutSection, TeamMember, Partner, Achievement, Member
from pathlib import Path
import os

class AboutDataTestCase(TestCase):
    def setUp(self):
        # Création des chemins pour les fichiers de test
        self.test_files_dir = Path(__file__).parent / 'test_files'
        self.test_files_dir.mkdir(exist_ok=True)

        # Création des fichiers de test
        self.create_test_images()

        # Create test users and members
        self.create_users_and_members()

        # Création des sections About
        self.create_about_sections()

        # Création des membres de l'équipe
        self.create_team_members()

        # Création des partenaires
        self.create_partners()

        # Création des réalisations
        self.create_achievements()

    def create_test_images(self):
        # Création d'images factices pour les tests
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # contenu vide pour le test
            content_type='image/jpeg'
        )

    def create_users_and_members(self):
        """Create test users and members with unique emails"""
        self.users_data = [
            {
                'email': 'president@save-asbl.org',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'role': 'president'
            },
            {
                'email': 'vice-president@save-asbl.org',
                'first_name': 'Marie',
                'last_name': 'Lambert',
                'role': 'vice_president'
            },
            {
                'email': 'secretary@save-asbl.org',
                'first_name': 'Pierre',
                'last_name': 'Martin',
                'role': 'secretary'
            }
        ]

        self.members = {}
        for user_data in self.users_data:
            role = user_data.pop('role')
            user = get_user_model().objects.create_user(
                password='testpass123',
                **user_data
            )
            member = Member.objects.create(
                user=user,
                membership_status='active',
                joined_at=timezone.now()
            )
            self.members[role] = member

    def create_about_sections(self):
        sections_data = [
            {
                'section_type': 'mission',
                'title': 'Notre Mission',
                'content': 'SAVE ASBL est dédiée au développement durable en RDC.',
                'subtitle': 'Construire un avenir meilleur',
                'order': 1
            },
            {
                'section_type': 'values',
                'title': 'Nos Valeurs',
                'content': 'Intégrité, Innovation, Solidarité',
                'order': 2
            },
            {
                'section_type': 'history',
                'title': 'Notre Histoire',
                'content': 'Fondée en 2024 avec une vision claire.',
                'order': 3
            }
        ]

        # Delete existing sections first
        AboutSection.objects.all().delete()

        # Create new sections
        for data in sections_data:
            AboutSection.objects.get_or_create(
                section_type=data['section_type'],
                defaults={
                    'image_main': self.test_image,
                    **data
                }
            )

    def create_team_members(self):
        """Create team members with their respective roles"""
        team_data = [
            {
                'member': self.members['president'],
                'role': 'president',
                'biography': 'Fondateur et visionnaire de SAVE ASBL.',
                'facebook': 'https://facebook.com/president',
                'linkedin': 'https://linkedin.com/in/president',
                'order': 1
            },
            {
                'member': self.members['vice_president'],
                'role': 'vice_president',
                'biography': 'Expert en développement durable avec plus de 10 ans d\'expérience.',
                'linkedin': 'https://linkedin.com/in/vice-president',
                'order': 2
            },
            {
                'member': self.members['secretary'],
                'role': 'secretary',
                'biography': 'Gestionnaire expérimenté et coordinateur de projets.',
                'linkedin': 'https://linkedin.com/in/secretary',
                'twitter': 'https://twitter.com/secretary',
                'order': 3
            }
        ]

        # Delete existing team members first
        TeamMember.objects.all().delete()

        # Create new team members
        for data in team_data:
            TeamMember.objects.create(**data)

    def create_partners(self):
        partners_data = [
            {
                'name': 'EcoTech RDC',
                'partnership_type': 'technical',
                'description': 'Partenaire technique principal',
                'website': 'https://ecotech-rdc.org'
            },
            {
                'name': 'Green Future',
                'partnership_type': 'strategic',
                'description': 'Partenaire stratégique',
                'website': 'https://green-future.org'
            }
        ]

        for data in partners_data:
            Partner.objects.create(
                logo=self.test_image,
                **data
            )

    def create_achievements(self):
        achievements_data = [
            {
                'title': 'Projets Réalisés',
                'description': 'Nombre de projets complétés en 2024',
                'metric_value': '25',
                'metric_label': 'projets',
                'year': 2024
            },
            {
                'title': 'Impact Environnemental',
                'description': 'Réduction des émissions de CO2',
                'metric_value': '500',
                'metric_label': 'tonnes de CO2',
                'year': 2024
            }
        ]

        for data in achievements_data:
            Achievement.objects.create(
                icon=self.test_image,
                **data
            )

    def test_about_data_creation(self):
        """Test la création des données About"""
        self.assertEqual(AboutSection.objects.count(), 3)
        self.assertEqual(TeamMember.objects.count(), 3)
        self.assertEqual(Partner.objects.count(), 2)
        self.assertEqual(Achievement.objects.count(), 2)

    def tearDown(self):
        # Nettoyage des fichiers de test
        if self.test_files_dir.exists():
            for file in self.test_files_dir.glob('*'):
                file.unlink()
            self.test_files_dir.rmdir()