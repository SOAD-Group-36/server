from random import randint
from django.core.management import BaseCommand
from django_seed import Seed

from products.models import Product
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
            Product,
            count,
            {
                'seller': Seller.objects.first(),
                'name': lambda x: seeder.faker.name(),
                'description': lambda x: seeder.faker.text(),
                'price': lambda x: seeder.faker.pyfloat(min_value=10.0),
                'length': lambda x: seeder.faker.pyint(min_value=10, max_value=9999),
                'stock': lambda x: seeder.faker.pyint(min_value=0, max_value=99),
                'weight': lambda x: seeder.faker.pyint(min_value=10, max_value=9999),
                'height': lambda x: seeder.faker.pyint(min_value=10, max_value=9999),
                
            },
        )
        seeder.execute()
