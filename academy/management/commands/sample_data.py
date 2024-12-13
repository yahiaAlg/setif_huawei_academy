from django.core.management.base import BaseCommand
from academy.models import Course, Certification, Contact

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Sample data for courses
        course_data = [
            {
                'title': 'Introduction à Python',
                'description': 'Un cours complet pour débutants couvrant les bases de Python, incluant les variables, les boucles, les fonctions et la programmation orientée objet.',
                'category': 'Programmation',
            },
            {
                'title': 'Data Science Avancée',
                'description': 'Apprenez les techniques avancées de data science incluant le machine learning, la visualisation de données et l\'analyse statistique.',
                'category': 'Data Science',
            },
            {
                'title': 'Développement Web avec Django',
                'description': 'Créez des applications web robustes avec Django, le framework Python le plus populaire pour le développement web.',
                'category': 'Web Development',
            },
            {
                'title': 'Intelligence Artificielle Fondamentale',
                'description': 'Découvrez les concepts fondamentaux de l\'IA, incluant les réseaux de neurones, le deep learning et le traitement du langage naturel.',
                'category': 'Intelligence Artificielle',
            },
            {
                'title': 'Cybersécurité Essentielle',
                'description': 'Apprenez les bases de la sécurité informatique, la cryptographie et la protection des données.',
                'category': 'Sécurité',
            }
        ]

        # Create courses
        for course in course_data:
            Course.objects.create(
                title=course['title'],
                description=course['description'],
                category=course['category'],
                # Note: You'll need to handle actual image files separately
            )

        # Sample data for certifications
        certification_data = [
            {
                'name': 'Python Developer Certification',
                'description': 'Certification professionnelle validant les compétences en développement Python',
                'level': 'Intermédiaire',
            },
            {
                'name': 'Data Scientist Professional',
                'description': 'Certification avancée en science des données et analyse',
                'level': 'Avancé',
            },
            {
                'name': 'Web Development Expert',
                'description': 'Certification expert en développement web full-stack',
                'level': 'Expert',
            },
            {
                'name': 'AI Fundamentals',
                'description': 'Certification de base en intelligence artificielle',
                'level': 'Débutant',
            }
        ]

        # Create certifications
        for cert in certification_data:
            Certification.objects.create(
                name=cert['name'],
                description=cert['description'],
                level=cert['level']
            )

        # Sample data for contacts
        contact_data = [
            {
                'name': 'Mohammed Amine',
                'email': 'amine@example.com',
                'subject': 'Question sur le cours Python',
                'message': 'Bonjour, j\'aimerais avoir plus d\'informations sur le cours de Python pour débutants.',
            },
            {
                'name': 'Sarah Benali',
                'email': 'sarah@example.com',
                'subject': 'Problème technique',
                'message': 'Je n\'arrive pas à accéder aux vidéos du cours de Data Science.',
            },
            {
                'name': 'Karim Hadj',
                'email': 'karim@example.com',
                'subject': 'Suggestion de cours',
                'message': 'Pourriez-vous ajouter un cours sur la blockchain ?',
            }
        ]

        # Create contacts
        for contact in contact_data:
            Contact.objects.create(
                name=contact['name'],
                email=contact['email'],
                subject=contact['subject'],
                message=contact['message']
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))