from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Project, CustomUser  # Import Project model
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the Project model with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate Project model...'))

        # Get or create a project manager (replace with an existing user if needed)
        project_manager, created = CustomUser.objects.get_or_create(
            email='project_manager_sante@example.com',  # Use email instead of username
            defaults={'first_name': 'Jean', 'last_name': 'Dupont'}
        )
        if created:
            project_manager.set_password('password123')
            project_manager.save()
            self.stdout.write(self.style.SUCCESS('Created project manager: Jean Dupont'))

        # Sample Projects
        projects_data = [
            {
                'title': 'Construction du Centre de Santé de Kinshasa',
                'project_code': 'SAVE-SANTE-2025-001',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=365),
                'status': 'active',
                'location': 'Kinshasa, RDC',
                'project_manager': project_manager,
                'budget': 150000.00,
                'funding_sources': 'Donateurs privés, Subventions gouvernementales',
                'goal': 'Améliorer l\'accès aux soins de santé de qualité pour les populations vulnérables de Kinshasa.',
                'objectives': 'Construire un centre de santé moderne et équipé, former du personnel médical qualifié, offrir des services de santé abordables.',
                'expected_impact': 'Réduction de la mortalité infantile, amélioration de la santé maternelle, prévention des maladies transmissibles.',
                'impact_indicators': 'Nombre de patients traités, taux de vaccination, taux de mortalité infantile.',
                'thematic_area': 'sante',
                'image': 'projects/default_project_image.jpg',  # Replace with actual image path
                'description': 'Ce projet vise à construire un centre de santé moderne à Kinshasa pour offrir des soins de qualité aux populations vulnérables.',
                'is_featured': True,
                'monitoring_plan': 'Suivi régulier des activités de construction, évaluation de la qualité des soins, collecte de données statistiques.',
                'evaluation_plan': 'Évaluation de l\'impact du projet sur la santé des populations, analyse des données statistiques, enquêtes auprès des bénéficiaires.',
                'risk_assessment': 'Risques liés à la construction, risques sanitaires, risques financiers.',
                'tech_stack': 'Utilisation de logiciels de gestion de la santé, télémédecine.',
                'sdg_goals': 'ODD 3',
            },
            {
                'title': 'Distribution de Fournitures Scolaires à Lubumbashi',
                'project_code': 'SAVE-EDU-2025-002',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=180),
                'status': 'completed',
                'location': 'Lubumbashi, RDC',
                'project_manager': project_manager,
                'budget': 50000.00,
                'funding_sources': 'Dons d\'entreprises locales, Collecte de fonds',
                'goal': 'Améliorer l\'accès à l\'éducation pour les enfants défavorisés de Lubumbashi.',
                'objectives': 'Distribuer des fournitures scolaires à 5000 enfants, sensibiliser les parents à l\'importance de l\'éducation, améliorer les résultats scolaires.',
                'expected_impact': 'Augmentation du taux de scolarisation, amélioration des résultats scolaires, réduction de l\'abandon scolaire.',
                'impact_indicators': 'Nombre d\'enfants ayant reçu des fournitures scolaires, taux de scolarisation, résultats aux examens.',
                'thematic_area': 'education',
                'image': 'projects/default_project_image.jpg',  # Replace with actual image path
                'description': 'Ce projet vise à distribuer des fournitures scolaires aux enfants défavorisés de Lubumbashi pour améliorer leur accès à l\'éducation.',
                'is_featured': False,
                'monitoring_plan': 'Suivi de la distribution des fournitures, collecte de données sur la fréquentation scolaire, évaluation des résultats scolaires.',
                'evaluation_plan': 'Évaluation de l\'impact du projet sur la scolarisation, analyse des résultats scolaires, enquêtes auprès des bénéficiaires.',
                'risk_assessment': 'Risques liés à la logistique, risques de détournement des fournitures, risques de faible participation.',
                'tech_stack': 'Utilisation d\'une plateforme de gestion des stocks, communication par SMS.',
                'sdg_goals': 'ODD 4',
            },
            {
                'title': 'Formation Agricole pour les Femmes à Goma',
                'project_code': 'SAVE-AGRI-2025-003',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=270),
                'status': 'active',
                'location': 'Goma, RDC',
                'project_manager': project_manager,
                'budget': 75000.00,
                'funding_sources': 'Subventions internationales, Partenariats avec des ONG',
                'goal': 'Autonomiser les femmes de Goma grâce à la formation agricole et à la création de coopératives.',
                'objectives': 'Former 200 femmes aux techniques agricoles modernes, créer 10 coopératives agricoles, améliorer la production agricole locale.',
                'expected_impact': 'Amélioration de la sécurité alimentaire, augmentation des revenus des femmes, développement économique local.',
                'impact_indicators': 'Nombre de femmes formées, nombre de coopératives créées, volume de la production agricole.',
                'thematic_area': 'agriculture',
                'image': 'projects/default_project_image.jpg',  # Replace with actual image path
                'description': 'Ce projet vise à former les femmes de Goma aux techniques agricoles modernes et à les aider à créer des coopératives pour améliorer leur autonomie économique.',
                'is_featured': True,
                'monitoring_plan': 'Suivi des formations, évaluation des compétences acquises, suivi de la production agricole.',
                'evaluation_plan': 'Évaluation de l\'impact du projet sur les revenus des femmes, analyse de la production agricole, enquêtes auprès des bénéficiaires.',
                'risk_assessment': 'Risques liés à la sécurité, risques climatiques, risques de faible participation.',
                'tech_stack': 'Utilisation d\'applications mobiles pour le suivi agricole, plateformes de vente en ligne.',
                'sdg_goals': 'ODD 5',
            },
        ]

        for data in projects_data:
            # Create the slug from the title
            data['slug'] = slugify(data['title'])
            project = Project.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated Project model.'))