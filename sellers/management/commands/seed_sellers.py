from django.core.management import BaseCommand
from django_seed import Seed

from sellers.models import Seller
from utils import Address

seeder = Seed.seeder()


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--count', default=1, type=int)

    def handle(self, *args, **options):
        count = options['count']
        seeder.add_entity(
            Seller,
            count,
            {
                'email': lambda x: seeder.faker.email(),
                'address': lambda x: Address('123456', 'State0', 'City0'),
            },
        )
        seeder.execute()
