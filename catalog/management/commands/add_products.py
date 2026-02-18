from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help("Add products in database")

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name="Категория_тест", description="Описание_тест")

        products = [
            {"name": "Товар_test",
             "description": "Описание",
             "category": category,
             "price": "123.00"
             },
            {"name": "Товар_7",
             "description": "Описание",
             "category": category,
             "price": "321.00"
             },
        ]

        for prod_data in products:
            prod, created = Product.objects.get_or_create(**prod_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added product: {prod.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Book already exist: {prod.name}"))
