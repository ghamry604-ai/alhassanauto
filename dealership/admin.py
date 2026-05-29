from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Car, CarImage


class CarImageInline(admin.TabularInline):
    """Inline editor for car images within the Car admin page."""
    model = CarImage
    extra = 3
    fields = ('image', 'caption', 'is_main', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'car_count', 'logo_preview', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('logo_preview',)

    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = 'Cars in Inventory'

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;" />', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Logo'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail', 'full_name', 'brand', 'year', 'price_display',
        'condition', 'transmission', 'fuel_type', 'is_available', 'is_featured', 'created_at'
    )
    list_display_links = ('thumbnail', 'full_name')
    list_filter = ('brand', 'condition', 'transmission', 'fuel_type', 'is_available', 'is_featured', 'year')
    search_fields = ('model_name', 'brand__name', 'color', 'description')
    list_editable = ('is_available', 'is_featured')
    prepopulated_fields = {'slug': ('brand', 'model_name', 'year')}
    inlines = [CarImageInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('brand', 'model_name', 'slug', 'year', 'color')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available', 'is_featured')
        }),
        ('Specifications', {
            'fields': ('condition', 'transmission', 'fuel_type', 'engine_size', 'horsepower', 'mileage')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return str(obj)
    full_name.short_description = 'Car'
    full_name.admin_order_field = 'model_name'

    def price_display(self, obj):
        return format_html('<strong style="color:#2563eb;">{}</strong>', obj.get_price_display())
    price_display.short_description = 'Price'
    price_display.admin_order_field = 'price'

    def thumbnail(self, obj):
        main_img = obj.get_main_image()
        if main_img:
            return format_html('<img src="{}" style="height:45px;width:70px;object-fit:cover;border-radius:4px;" />', main_img.image.url)
        return format_html('<div style="height:45px;width:70px;background:#e5e7eb;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#6b7280;">No Image</div>')
    thumbnail.short_description = ''


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'car', 'caption', 'is_main', 'order', 'uploaded_at')
    list_filter = ('is_main', 'car__brand')
    search_fields = ('car__model_name', 'caption')
    list_editable = ('is_main', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;width:80px;object-fit:cover;border-radius:4px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


# Customize admin site header
admin.site.site_header = 'AutoElite Dealership Admin'
admin.site.site_title = 'AutoElite Admin'
admin.site.index_title = 'Dealership Management'
