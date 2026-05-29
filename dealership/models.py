from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    """Represents a car manufacturer brand."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Car(models.Model):
    """Represents a car listing in the dealership inventory."""

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('certified', 'Certified Pre-Owned'),
    ]

    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('cvt', 'CVT'),
        ('semi_auto', 'Semi-Automatic'),
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('plugin_hybrid', 'Plug-in Hybrid'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model_name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(default=0, help_text='Mileage in kilometers')
    color = models.CharField(max_length=50, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='used')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    engine_size = models.CharField(max_length=20, blank=True, help_text='e.g. 2.0L, 1600cc')
    horsepower = models.PositiveIntegerField(blank=True, null=True, help_text='Horsepower (HP)')
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.model_name}-{self.year}")
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_main_image(self):
        """Returns the main image or first available image."""
        main = self.images.filter(is_main=True).first()
        if main:
            return main
        return self.images.first()

    def get_price_display(self):
        return f"${self.price:,.0f}"

    def __str__(self):
        return f"{self.year} {self.brand.name} {self.model_name}"


class CarImage(models.Model):
    """Stores multiple images per car listing."""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False, help_text='Set as the primary display image')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_main', 'order']
        verbose_name = 'Car Image'
        verbose_name_plural = 'Car Images'

    def save(self, *args, **kwargs):
        # Ensure only one main image per car
        if self.is_main:
            CarImage.objects.filter(car=self.car, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.car} ({'Main' if self.is_main else 'Gallery'})"
