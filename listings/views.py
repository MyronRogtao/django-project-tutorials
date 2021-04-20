from django.shortcuts import render
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Enquiry
from datetime import date
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.
def listings(request):
    available_listings = Listing.objects\
        .filter(is_published=True)\
        .order_by('-list_date')

    # paginator = Paginator(available_listings, 3)
    # page = request.GET.get('page')
    # paged_list = paginator.get_page(page)
    return render(request, 'listings/index.html', {
        'activated': 'Listings',
        'listings': available_listings
    })


def listing(request, listing_id):
    selected_listing = Listing.objects.get(pk=listing_id)
    return render(request, 'listings/listing.html', {
        'activated': 'Listings',
        'listing': selected_listing,
        'title': selected_listing.title,
        'address': selected_listing.address
    })


def search(request):
    filter_options = {
        "states": {},
        "bedrooms": {},
        "max_prices": [1000000, 3000000, 5000000, 7000000, 9000000, 10000000]
    }
    option_listings = Listing.objects.all()
    filter_options["states"] = sorted({option_listing.state for option_listing in option_listings})
    filter_options["bedrooms"] = sorted({option_listing.bedrooms for option_listing in option_listings})

    # keywords
    option_listings = filter_helper('keywords',
                                    lambda param, data: option_listings.filter(description__icontains=param),
                                    option_listings,
                                    request)
    # city
    option_listings = filter_helper('city',
                                    lambda param, data: option_listings.filter(city__iexact=param),
                                    option_listings,
                                    request)

    # state
    option_listings = filter_helper('state',
                                    lambda param, data: option_listings.filter(state__iexact=param),
                                    option_listings,
                                    request)
    # bedroom
    option_listings = filter_helper('bedrooms',
                                    lambda param, data: option_listings.filter(bedrooms=param),
                                    option_listings,
                                    request)
    # price
    option_listings = filter_helper('price',
                                    lambda param, data: option_listings.filter(price__lte=param),
                                    option_listings,
                                    request)
    return render(request, 'listings/search.html', {
        'activated': 'Listings',
        'filter_options': filter_options,
        'listings': option_listings,
        'values': request.GET
        })


def filter_helper(field, filter_fn, data, request):
    if field in request.GET:
        filter_value = request.GET[field]
        if filter_value:
            return filter_fn(filter_value, data)

    return data


def enquire(request, listing_id):
    if request.method == 'POST':
        phone = request.POST['phone']
        message = request.POST['message']
        enquired_listing = Listing.objects.get(pk=listing_id)

        enquiry = Enquiry(message=message, phone=phone, listing=enquired_listing, contact_date=date.today())

        if request.user.is_authenticated:
            enquiry.user_id = request.user.id
            enquiry.name = request.user.first_name
            enquiry.email = request.user.email
        else:
            enquiry.name = request.POST['name']
            enquiry.email = request.POST['email']

        if enquiry.user_id:
            enquiry_present = Enquiry.objects.filter(user_id=enquiry.user_id, listing__id=listing_id).exists()
            if enquiry_present:
                messages.error(request, "Inquiry already made for this property")
                return redirect('listings:listing', listing_id)
        enquiry.save()
        send_email(enquiry)
        messages.success(request, "Inquiry submitted successfully")
        return redirect('listings:listing', listing_id)

    messages.error(request, "Unable to submit Inquiry.Try again after some time")
    return redirect('listings:listing', listing_id)


def send_email(enquiry):
    realtor_address = enquiry.listing.realtor.email
    subject = 'Property Inquiry'
    from_address = 'test@mmre.com'
    template = 'Property : {title}\n\nInquiry By:\nName: {name}\nPhone: {phone}\nEmail: {email}\nQuery: {query}\n'
    body = template.replace('{title}', enquiry.listing.title)\
        .replace('{name}', enquiry.name) \
        .replace('{phone}', enquiry.phone) \
        .replace('{email}', enquiry.email) \
        .replace('{query}', enquiry.message)
    send_mail(subject, body, from_address, (realtor_address,), fail_silently=False)
