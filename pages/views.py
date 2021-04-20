from django.shortcuts import render
from realtors.models import Realtor
from listings.models import Listing


# Create your views here.
def index(request):
    filter_options = {
        "states": {},
        "bedrooms": {},
        "max_prices": [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]
    }
    latest_listings = Listing.objects\
        .filter(is_published=True)\
        .order_by('-list_date')[:3]

    listings = Listing.objects.all()
    filter_options["states"] = sorted({listing.state for listing in listings})
    filter_options["bedrooms"] = sorted({listing.bedrooms for listing in listings})

    return render(request, 'pages/index.html', {
        'activated': 'Home',
        'latest_listings': latest_listings,
        'filter_options': filter_options
    })


def about(request):
    realtors = Realtor.objects.all()[:]
    mvp = next(filter(lambda realtor: realtor.is_mvp, realtors), None)
    return render(request, 'pages/about.html', {
        'activated': 'About',
        'realtors': realtors,
        'mvp': mvp
    })
