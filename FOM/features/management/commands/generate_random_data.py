# Import necessary modules
import random
from faker import Faker
from django.core.management.base import BaseCommand
from features.models import CommonClient, CommonFeature
from datetime import datetime , timedelta

class Command(BaseCommand):
    help = 'Generate and add random data to the database'

    def handle(self, *args, **kwargs):
        # Initialize Faker generator
        fake = Faker()

        # Generate random CommonClient data
        self.generate_random_clients(fake)

        # Generate random CommonFeature data
        self.generate_random_features(fake)

        self.stdout.write(self.style.SUCCESS('Random data generation complete.'))

    def generate_random_clients(self, fake):
        for _ in range(200):  # Generate 200 clients, adjust the number as needed
            name = fake.name()
            active = fake.boolean(chance_of_getting_true=50)
            lot_prefix = fake.word()
            username_prefix_code = fake.word()
            dispatch_date_freeze = fake.date_between(start_date='-30y', end_date='today')
            formal_name = fake.company()

            # Create and save a new CommonClient instance
            client = CommonClient.objects.create(
                name=name,
                active=active,
                lot_prefix=lot_prefix,
                username_prefix_code=username_prefix_code,
                dispatch_date_freeze=dispatch_date_freeze,
                formal_name=formal_name
            )

            self.stdout.write(self.style.SUCCESS(f'Client "{client.name}" created.'))

    def generate_random_features(self, fake):
        for _ in range(200):  # Generate 10 features, adjust the number as needed
            name = fake.word()
            default_value = fake.word()
            value_type = random.choice(['Integer', 'String', 'Boolean'])
            description = fake.sentence()

            # Create and save a new CommonFeature instance
            feature = CommonFeature.objects.create(
                name=name,
                default_value=default_value,
                value_type=value_type,
                description=description
            )

            self.stdout.write(self.style.SUCCESS(f'Feature "{feature.name}" created.'))

