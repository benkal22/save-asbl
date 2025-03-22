from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Activity, CustomUser  # Import Activity model
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the Activity model with sample data'  # Update help text

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate Activity model...'))  # Update message

        # Get or create a activity manager (replace with an existing user if needed)
        activity_manager, created = CustomUser.objects.get_or_create(  # Update variable name
            email='activity_manager_sante@example.com',
            defaults={'first_name': 'Jean', 'last_name': 'Dupont'}
        )
        if created:
            activity_manager.set_password('password123')  # Update variable name
            activity_manager.save()  # Update variable name
            self.stdout.write(self.style.SUCCESS('Created activity manager: Jean Dupont'))  # Update message

        # Sample Activities
        activities_data = [  # Update variable name
            {
                'title': 'Santé',
                'activity_code': 'SAVE-ACT-2025-001',  # Update field name
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=365),
                'status': 'active',
                'location': 'République Démocratique du Congo',
                'activity_manager': activity_manager,  # Update variable name
                'budget': 200000.00,
                'funding_sources': 'Donateurs privés, Subventions gouvernementales',
                'goal': 'Défendre et promouvoir les intérêts de la population dans le domaine de la santé.',
                'objectives': 'Création de centres hospitaliers, mise à disposition de produits pharmaceutiques et de matériel médical, lutte contre l\'insalubrité publique.',
                'expected_impact': 'Amélioration de l\'accès aux soins de santé, réduction des maladies, amélioration de l\'environnement sanitaire.',
                'impact_indicators': 'Nombre de patients traités, taux de vaccination, réduction des maladies liées à l\'insalubrité.',
                'thematic_area': 'sante',
                'image': 'activities/default_activity_image.jpg',  # Replace with actual image path
                'description': 'SAVE ASBL défend et promeut les intérêts de la population dans le domaine de la santé. Nos actions incluent : Création de centres hospitaliers, mise à disposition de produits pharmaceutiques et de matériel médical, lutte contre l\'insalubrité publique pour un environnement sain.',
                'is_featured': True,
                'monitoring_plan': 'Suivi régulier des activités, évaluation de la qualité des soins, collecte de données statistiques.',
                'evaluation_plan': "Évaluation de l'impact de l'activité sur la santé des populations, analyse des données statistiques, enquêtes auprès des bénéficiaires.",  # Corrected line
                'risk_assessment': 'Risques liés à la logistique, risques sanitaires, risques financiers.',
                'tech_stack': 'Utilisation de logiciels de gestion de la santé, télémédecine.',
                'sdg_goals': 'ODD 3',
            },
            {
                'title': 'Éducation',
                'activity_code': 'SAVE-ACT-2025-002',  # Update field name
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=365),
                'status': 'active',
                'location': 'République Démocratique du Congo',
                'activity_manager': activity_manager,  # Update variable name
                'budget': 150000.00,
                'funding_sources': 'Dons d\'entreprises locales, Collecte de fonds',
                'goal': 'Lutter contre l\'analphabétisme et soutenir l\'éducation.',
                'objectives': 'Mise à disposition de fournitures scolaires et de matériel didactique, construction et restauration d\'écoles, initiation aux logiciels de base et création de centres informatiques.',
                'expected_impact': 'Augmentation du taux de scolarisation, amélioration des résultats scolaires, réduction de l\'analphabétisme.',
                'impact_indicators': 'Nombre d\'enfants ayant reçu des fournitures scolaires, taux de scolarisation, résultats aux examens.',
                'thematic_area': 'education',
                'image': 'activities/default_activity_image.jpg',  # Replace with actual image path
                'description': 'Nous luttons contre l\'analphabétisme et soutenons l\'éducation à travers : Mise à disposition de fournitures scolaires et de matériel didactique, construction et restauration d\'écoles, initiation aux logiciels de base et création de centres informatiques.',
                'is_featured': True,
                'monitoring_plan': 'Suivi de la distribution des fournitures, évaluation de la fréquentation scolaire, évaluation des compétences acquises.',
                'evaluation_plan': "Évaluation de l'impact de l'activité sur la scolarisation, analyse des résultats scolaires, enquêtes auprès des bénéficiaires.",  # Corrected line
                'risk_assessment': 'Risques liés à la logistique, risques de détournement des fournitures, risques de faible participation.',
                'tech_stack': 'Utilisation d\'une plateforme de gestion des stocks, communication par SMS.',
                'sdg_goals': 'ODD 4',
            },
            {
                'title': 'Agriculture',
                'activity_code': 'SAVE-ACT-2025-003',  # Update field name
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=365),
                'status': 'active',
                'location': 'République Démocratique du Congo',
                'activity_manager': activity_manager,  # Update variable name
                'budget': 100000.00,
                'funding_sources': 'Subventions internationales, Partenariats avec des ONG',
                'goal': 'Soutenir l\'agriculture et lutter contre la faim.',
                'objectives': 'Promotion de pratiques modernes d\'élevage et d\'agriculture, appui aux agriculteurs avec du matériel moderne, aménagement de routes de desserte agricole.',
                'expected_impact': 'Amélioration de la sécurité alimentaire, augmentation des revenus des agriculteurs, développement économique local.',
                'impact_indicators': 'Volume de la production agricole, revenus des agriculteurs, nombre de routes de desserte agricole aménagées.',
                'thematic_area': 'agriculture',
                'image': 'activities/default_activity_image.jpg',  # Replace with actual image path
                'description': 'Nous soutenons l\'agriculture et luttons contre la faim grâce à : Promotion de pratiques modernes d\'élevage et d\'agriculture, appui aux agriculteurs avec du matériel moderne, aménagement de routes de desserte agricole.',
                'is_featured': True,
                'monitoring_plan': 'Suivi des formations, évaluation des compétences acquises, suivi de la production agricole.',
                'evaluation_plan': "Évaluation de l'impact de l'activité sur les revenus des agriculteurs, analyse de la production agricole, enquêtes auprès des bénéficiaires.",  # Corrected line
                'risk_assessment': 'Risques liés à la sécurité, risques climatiques, risques de faible participation.',
                'tech_stack': 'Utilisation d\'applications mobiles pour le suivi agricole, plateformes de vente en ligne.',
                'sdg_goals': 'ODD 2',
            },
            {
                'title': 'Émancipation de la femme',
                'activity_code': 'SAVE-ACT-2025-004',  # Update field name
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=365),
                'status': 'active',
                'location': 'République Démocratique du Congo',
                'activity_manager': activity_manager,  # Update variable name
                'budget': 75000.00,
                'funding_sources': 'Subventions internationales, Dons de particuliers',
                'goal': 'Œuvrer pour l\'émancipation de la femme et l\'épanouissement de la famille.',
                'objectives': 'Sensibilisation aux droits de la femme et de la famille, apprentissage de métiers et création de coopératives, promotion de l\'égalité des genres.',
                'expected_impact': 'Amélioration de la condition féminine, autonomisation économique des femmes, promotion de l\'égalité des genres.',
                'impact_indicators': 'Nombre de femmes sensibilisées, nombre de femmes ayant appris un métier, nombre de coopératives créées.',
                'thematic_area': 'femme_famille',
                'image': 'activities/default_activity_image.jpg',  # Replace with actual image path
                'description': 'Nous œuvrons pour l\'émancipation de la femme et l\'épanouissement de la famille à travers : Sensibilisation aux droits de la femme et de la famille, apprentissage de métiers et création de coopératives, promotion de l\'égalité des genres.',
                'is_featured': True,
                'monitoring_plan': 'Suivi des formations, évaluation des compétences acquises, suivi de la création de coopératives.',
                'evaluation_plan': "Évaluation de l'impact de l'activité sur la condition féminine, analyse des revenus des femmes, enquêtes auprès des bénéficiaires.",  # Corrected line
                'risk_assessment': 'Risques liés à la sécurité, risques de faible participation, risques de discrimination.',
                'tech_stack': 'Utilisation d\'applications mobiles pour la formation, plateformes de vente en ligne.',
                'sdg_goals': 'ODD 5',
            },
        ]

        for data in activities_data:  # Update variable name
            # Create the slug from the title
            data['slug'] = slugify(data['title'])
            activity = Activity.objects.create(**data)  # Update model name
            self.stdout.write(self.style.SUCCESS(f'Created activity: {activity.title}'))  # Update message

        self.stdout.write(self.style.SUCCESS('Successfully populated Activity model.'))  # Update message