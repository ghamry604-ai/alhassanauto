from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Brand, Car


def homepage(request):
    """Homepage: featured cars + latest arrivals."""
    featured_cars = Car.objects.filter(is_available=True, is_featured=True).select_related('brand')[:6]
    latest_cars = Car.objects.filter(is_available=True).select_related('brand').prefetch_related('images')[:8]
    brands = Brand.objects.all()
    stats = {
        'total_cars': Car.objects.filter(is_available=True).count(),
        'total_brands': Brand.objects.count(),
        'new_cars': Car.objects.filter(is_available=True, condition='new').count(),
    }

    context = {
        'featured_cars': featured_cars,
        'latest_cars': latest_cars,
        'brands': brands,
        'stats': stats,
        'condition_choices': Car.CONDITION_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,
        'page_title': 'AutoElite — Premium Car Dealership',
    }
    return render(request, 'dealership/home.html', context)


def car_list(request):
    """Car listings page with filtering and pagination."""
    cars = Car.objects.filter(is_available=True).select_related('brand').prefetch_related('images')

    # --- Filtering ---
    brand_slug = request.GET.get('brand', '')
    condition = request.GET.get('condition', '')
    fuel_type = request.GET.get('fuel_type', '')
    transmission = request.GET.get('transmission', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '-created_at')

    if brand_slug:
        cars = cars.filter(brand__slug=brand_slug)
    if condition:
        cars = cars.filter(condition=condition)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if min_price:
        try:
            cars = cars.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            cars = cars.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    valid_sorts = ['-created_at', 'created_at', 'price', '-price', 'year', '-year']
    if sort in valid_sorts:
        cars = cars.order_by(sort)

    # Pagination
    paginator = Paginator(cars, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'brands': Brand.objects.all(),
        'condition_choices': Car.CONDITION_CHOICES,
        'fuel_choices': Car.FUEL_CHOICES,
        'transmission_choices': Car.TRANSMISSION_CHOICES,
        'current_filters': {
            'brand': brand_slug,
            'condition': condition,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
        },
        'total_count': cars.count(),
        'page_title': 'Browse Cars — AutoElite',
    }
    return render(request, 'dealership/car_list.html', context)


def car_detail(request, slug):
    """Single car detail page."""
    car = get_object_or_404(
        Car.objects.select_related('brand').prefetch_related('images'),
        slug=slug,
        is_available=True
    )
    images = car.images.all()
    main_image = car.get_main_image()

    # Related cars: same brand, exclude current
    related_cars = Car.objects.filter(
        brand=car.brand,
        is_available=True
    ).exclude(pk=car.pk).prefetch_related('images')[:4]

    context = {
        'car': car,
        'images': images,
        'main_image': main_image,
        'related_cars': related_cars,
        'page_title': f"{car} — AutoElite",
        'specs': [
            ('Year', car.year),
            ('Condition', car.get_condition_display()),
            ('Transmission', car.get_transmission_display()),
            ('Fuel Type', car.get_fuel_type_display()),
            ('Engine', car.engine_size or '—'),
            ('Horsepower', f"{car.horsepower} HP" if car.horsepower else '—'),
            ('Mileage', f"{car.mileage:,} km" if car.mileage else '0 km'),
            ('Color', car.color or '—'),
        ],
    }
    return render(request, 'dealership/car_detail.html', context)
