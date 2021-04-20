from django.db import models
from datetime import datetime
from realtors.models import Realtor


# Create your models here.
class Listing(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    price = models.IntegerField(null=False)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    garage = models.IntegerField()
    sq_ft = models.IntegerField()
    lot_size = models.FloatField()
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now)
    realtor = models.ForeignKey(Realtor, on_delete= models.DO_NOTHING)

    def get_main_image(self):
        main_img = ''
        for img in self.listingimage_set.all():
            main_img = img.image if img.is_main else ''
            if main_img:
                break
        return main_img

    def __str__(self):
        return self.title


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='listings/%Y/%m/%d/')
    is_main = models.BooleanField(default=False)


class Enquiry(models.Model):
    user_id = models.IntegerField(null=True)
    listing = models.ForeignKey(Listing, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    contact_date = models.DateField()

