from django.core.management.base import BaseCommand
from dealership.models import Brand, Car


class Command(BaseCommand):
    help = 'Seeds the database with sample brands and cars'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Clear existing
        Car.objects.all().delete()
        Brand.objects.all().delete()

        brands_data = [
            'Toyota', 'BMW', 'Mercedes-Benz', 'Ford', 'Honda', 'Audi', 'Chevrolet', 'Porsche'
        ]
        brands = {}
        for name in brands_data:
            b = Brand.objects.create(name=name)
            brands[name] = b

        cars = [
            {'brand': 'Toyota', 'model_name': 'Camry', 'year': 2023, 'price': 28500, 'condition': 'new', 'transmission': 'automatic', 'fuel_type': 'petrol', 'mileage': 0, 'color': 'Silver', 'horsepower': 203, 'engine_size': '2.5L', 'is_featured': True},
            {'brand': 'BMW', 'model_name': '3 Series', 'year': 2022, 'price': 47900, 'condition': 'used', 'transmission': 'automatic', 'fuel_type': 'petrol', 'mileage': 22000, 'color': 'Black', 'horsepower': 255, 'engine_size': '2.0L', 'is_featured': True},
            {'brand': 'Mercedes-Benz', 'model_name': 'C-Class', 'year': 2023, 'price': 55000, 'condition': 'new', 'transmission': 'automatic', 'fuel_type': 'hybrid', 'mileage': 0, 'color': 'White', 'horsepower': 300, 'engine_size': '1.5L', 'is_featured': True},
            {'brand': 'Ford', 'model_name': 'Mustang GT', 'year': 2021, 'price': 38750, 'condition': 'used', 'transmission': 'manual', 'fuel_type': 'petrol', 'mileage': 35000, 'color': 'Red', 'horsepower': 450, 'engine_size': '5.0L'},
            {'brand': 'Honda', 'model_name': 'Civic', 'year': 2022, 'price': 24500, 'condition': 'certified', 'transmission': 'cvt', 'fuel_type': 'petrol', 'mileage': 18000, 'color': 'Blue', 'horsepower': 158, 'engine_size': '1.5L'},
            {'brand': 'Audi', 'model_name': 'A4 Quattro', 'year': 2022, 'price': 44000, 'condition': 'used', 'transmission': 'automatic', 'fuel_type': 'petrol', 'mileage': 28000, 'color': 'Gray', 'horsepower': 201, 'engine_size': '2.0L', 'is_featured': True},
            {'brand': 'Chevrolet', 'model_name': 'Corvette Stingray', 'year': 2023, 'price': 72000, 'condition': 'new', 'transmission': 'automatic', 'fuel_type': 'petrol', 'mileage': 0, 'color': 'Yellow', 'horsepower': 495, 'engine_size': '6.2L', 'is_featured': True},
            {'brand': 'Porsche', 'model_name': 'Cayenne', 'year': 2022, 'price': 89500, 'condition': 'used', 'transmission': 'automatic', 'fuel_type': 'hybrid', 'mileage': 15000, 'color': 'Black', 'horsepower': 455, 'engine_size': '3.0L', 'is_featured': True},
            {'brand': 'Toyota', 'model_name': 'RAV4 Hybrid', 'year': 2023, 'price': 33000, 'condition': 'new', 'transmission': 'cvt', 'fuel_type': 'hybrid', 'mileage': 0, 'color': 'Green', 'horsepower': 219, 'engine_size': '2.5L'},
            {'brand': 'BMW', 'model_name': 'X5 xDrive', 'year': 2021, 'price': 62000, 'condition': 'certified', 'transmission': 'automatic', 'fuel_type': 'diesel', 'mileage': 40000, 'color': 'White', 'horsepower': 340, 'engine_size': '3.0L'},
            {'brand': 'Ford', 'model_name': 'F-150 Raptor', 'year': 2022, 'price': 68000, 'condition': 'used', 'transmission': 'automatic', 'fuel_type': 'petrol', 'mileage': 20000, 'color': 'Gray', 'horsepower': 450, 'engine_size': '3.5L'},
            {'brand': 'Honda', 'model_name': 'CR-V', 'year': 2023, 'price': 31000, 'condition': 'new', 'transmission': 'automatic', 'fuel_type': 'hybrid', 'mileage': 0, 'color': 'Silver', 'horsepower': 204, 'engine_size': '2.0L'},
        ]

        for c in cars:
            brand = brands[c.pop('brand')]
            Car.objects.create(brand=brand, **c)

        self.stdout.write(self.style.SUCCESS(f'✓ Created {Brand.objects.count()} brands and {Car.objects.count()} cars.'))
        self.stdout.write(self.style.WARNING('Note: No images were added. Upload images via the admin panel.'))
